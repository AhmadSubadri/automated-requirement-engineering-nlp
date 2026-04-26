import time
import re
import torch
from transformers import pipeline

# ── Kategori NFR ─────────────────────────────────────────────
NFR_KEYWORDS = {
    'Performance': ['cepat', 'lambat', 'response time', 'speed', 'fast', 'performa',
                    'throughput', 'latency', 'waktu respon', 'detik', 'milidetik'],
    'Security':    ['keamanan', 'security', 'enkripsi', 'encryption', 'password',
                    'autentikasi', 'authentication', 'otorisasi', 'authorization',
                    'ssl', 'token', 'hak akses', 'privilege'],
    'Usability':   ['mudah', 'antarmuka', 'interface', 'ui', 'user friendly',
                    'tampilan', 'navigasi', 'intuitif', 'responsive'],
    'Reliability': ['handal', 'reliable', 'backup', 'recovery', 'stabil', 'stable',
                    'uptime', 'availability', 'fault', 'error handling'],
    'Scalability': ['skala', 'scale', 'kapasitas', 'capacity', 'load', 'beban',
                    'concurrent', 'pengguna bersamaan'],
    'Maintainability': ['maintainable', 'dokumentasi', 'modular', 'log', 'monitoring'],
}

NFR_ALL_KEYWORDS = [kw for kws in NFR_KEYWORDS.values() for kw in kws]

MOSCOW_KEYWORDS = {
    'Must Have':   ['harus', 'must', 'wajib', 'shall', 'required', 'kritis', 'mandatory'],
    'Should Have': ['sebaiknya', 'should', 'disarankan', 'recommended', 'penting'],
    'Could Have':  ['bisa', 'could', 'opsional', 'optional', 'tambahan', 'nice to have'],
    "Won't Have":  ['tidak perlu', "won't", 'future', 'nanti', 'belum', 'fase berikutnya'],
}

# ── Model configs (versi ringan untuk CPU) ───────────────────
MODEL_CONFIGS = {
    'BERT':       'bert-base-uncased',
    'RoBERTa':    'distilroberta-base',
    'DistilBERT': 'distilbert-base-uncased',
}


def load_models():
    """
    Load 3 model transformer untuk klasifikasi teks.
    Dioptimasi untuk CPU: no_grad, max_length=128, batch_size=1
    """
    models = {}
    for name, model_id in MODEL_CONFIGS.items():
        try:
            clf = pipeline(
                "text-classification",
                model=model_id,
                tokenizer=model_id,
                return_all_scores=True,
                device=-1,          # paksa CPU
                truncation=True,
                max_length=128,     # hemat komputasi
            )
            models[name] = {'pipeline': clf, 'status': 'loaded'}
        except Exception as e:
            models[name] = {'pipeline': None, 'status': f'error: {str(e)}'}
    return models


def classify_rule_based(text):
    """Klasifikasi berbasis keyword sebagai fallback"""
    text_lower = text.lower()
    for kw in NFR_ALL_KEYWORDS:
        if kw in text_lower:
            return 'Non-Functional'
    return 'Functional'


def get_nfr_category(text):
    text_lower = text.lower()
    for category, keywords in NFR_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return category
    return 'General'


def get_priority(text):
    text_lower = text.lower()
    for priority, keywords in MOSCOW_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return priority
    return 'Should Have'


def run_model_classification(text, model_entry):
    """Jalankan satu model, return dict hasil"""
    start = time.time()

    if model_entry['pipeline'] is None:
        req_type = classify_rule_based(text)
        return {
            'type': req_type,
            'confidence': 70.0,
            'inference_time_ms': 0,
            'method': 'rule-based (model gagal load)'
        }

    try:
        with torch.no_grad():
            output = model_entry['pipeline'](text[:512])

        elapsed = round((time.time() - start) * 1000, 1)
        scores = output[0]
        best = max(scores, key=lambda x: x['score'])

        # Mapping label → FR / NFR
        # Model umum tidak dilatih FR/NFR, jadi kita pakai
        # skor tertinggi + rule-based sebagai tiebreaker
        rule_type = classify_rule_based(text)
        confidence = round(best['score'] * 100, 1)

        # Jika confidence model rendah (< 60%), percayai rule-based
        if confidence < 60:
            final_type = rule_type
        else:
            # Label_0 biasanya NEGATIVE/class-0 → kita map ke Functional
            # karena majority requirement adalah Functional
            label_map = {
                'LABEL_0': 'Functional',
                'LABEL_1': 'Non-Functional',
                'POSITIVE': 'Functional',
                'NEGATIVE': 'Non-Functional',
            }
            mapped = label_map.get(best['label'])
            final_type = mapped if mapped else rule_type

        return {
            'type': final_type,
            'confidence': confidence,
            'inference_time_ms': elapsed,
            'method': 'transformer'
        }

    except Exception as e:
        req_type = classify_rule_based(text)
        return {
            'type': req_type,
            'confidence': 65.0,
            'inference_time_ms': 0,
            'method': f'rule-based (error: {str(e)[:40]})'
        }


def analyze_requirements(requirements, models):
    """
    Jalankan 3 model sekaligus untuk setiap requirement.
    Return list requirement yang sudah dilengkapi hasil analisis.
    """
    analyzed = []

    for req in requirements:
        text = req['text']
        model_results = {}

        for model_name in ['BERT', 'RoBERTa', 'DistilBERT']:
            model_entry = models.get(model_name, {'pipeline': None})
            result = run_model_classification(text, model_entry)
            model_results[model_name] = result

        # Voting majority dari 3 model
        types = [r['type'] for r in model_results.values()]
        final_type = max(set(types), key=types.count)
        avg_conf = round(
            sum(r['confidence'] for r in model_results.values()) / len(model_results), 1
        )
        consensus = (len(set(types)) == 1)

        analyzed.append({
            **req,
            'type': final_type,
            'nfr_category': get_nfr_category(text) if final_type == 'Non-Functional' else '-',
            'priority': get_priority(text),
            'model_results': model_results,
            'avg_confidence': avg_conf,
            'consensus': consensus,
            'quality_score': 100,   # akan diisi oleh validation module
        })

    return analyzed