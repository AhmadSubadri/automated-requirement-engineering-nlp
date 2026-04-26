import re
from utils.file_parser import split_sentences

# ── Pola keyword requirement ─────────────────────────────────
REQUIREMENT_PATTERNS = [
    r'\b(sistem|system)\s+(harus|shall|must|should|akan|will|dapat|bisa)\b',
    r'\b(harus|must|shall|wajib|perlu|required)\b',
    r'\b(pengguna|user|admin|administrator|operator)\s+(dapat|bisa|could|mampu|harus)\b',
    r'\b(fitur|feature|fungsi|function|modul|module|fasilitas)\b',
    r'\b(dapat|bisa|mampu|able to|capable of)\b',
    r'\b(input|output|proses|process|tampil|display|simpan|save|kirim|send)\b',
    r'\b(login|logout|register|upload|download|kelola|manage|laporan|report)\b',
]

ACTORS = [
    'admin', 'administrator', 'pengguna', 'user', 'sistem', 'system',
    'manager', 'staff', 'customer', 'pelanggan', 'operator', 'superadmin',
    'kasir', 'guru', 'siswa', 'dokter', 'pasien'
]

ACTIONS = [
    'login', 'logout', 'register', 'daftar', 'upload', 'download',
    'tambah', 'hapus', 'edit', 'ubah', 'lihat', 'kelola', 'manage',
    'input', 'output', 'proses', 'kirim', 'terima', 'validasi',
    'cari', 'search', 'filter', 'ekspor', 'impor', 'laporan', 'cetak',
    'approve', 'reject', 'konfirmasi', 'bayar', 'verifikasi'
]


def extract_actor(sentence):
    sentence_lower = sentence.lower()
    for actor in ACTORS:
        if actor in sentence_lower:
            return actor.capitalize()
    return 'System'


def extract_action(sentence):
    sentence_lower = sentence.lower()
    for action in ACTIONS:
        if action in sentence_lower:
            return action.capitalize()
    return 'Proses'


def extract_requirements(text):
    """Ekstrak kandidat requirement dari teks input"""
    sentences = split_sentences(text)
    requirements = []
    req_counter = 1

    for sentence in sentences:
        score = sum(
            1 for pattern in REQUIREMENT_PATTERNS
            if re.search(pattern, sentence, re.IGNORECASE)
        )

        if score >= 1:
            requirements.append({
                'id': f'REQ-{str(req_counter).zfill(3)}',
                'text': sentence,
                'actor': extract_actor(sentence),
                'action': extract_action(sentence),
                'relevance_score': score,
                'source': f'Auto-extracted',
                'status': 'pending'
            })
            req_counter += 1

    return requirements