import re

AMBIGUOUS_WORDS = [
    'cepat', 'lambat', 'mudah', 'sulit', 'besar', 'kecil', 'banyak', 'sedikit',
    'bagus', 'baik', 'buruk', 'optimal', 'maksimal tanpa ukuran',
    'fast', 'slow', 'easy', 'difficult', 'good', 'bad', 'quickly',
    'beberapa', 'some', 'several', 'various', 'appropriate', 'sesuai', 'proper',
    'memadai', 'layak', 'wajar',
]

MEASURABLE_PATTERNS = [
    r'\d+\s*(detik|menit|jam|second|minute|hour|ms|millisecond)',
    r'\d+\s*(%|persen|percent)',
    r'\d+\s*(mb|gb|kb|tb)',
    r'\d+\s*(user|pengguna|request|transaksi|concurrent)',
    r'kurang dari|lebih dari|minimal|maksimal|paling lambat|paling cepat',
    r'less than|more than|minimum|maximum|at least|at most',
    r'\d+x|\d+ kali',
]

ACTOR_KEYWORDS = [
    'user', 'pengguna', 'admin', 'administrator', 'sistem', 'system',
    'operator', 'manager', 'staff', 'customer', 'pelanggan',
    'kasir', 'guru', 'siswa', 'dokter', 'pasien', 'superadmin'
]

ACTION_KEYWORDS = [
    'dapat', 'harus', 'must', 'shall', 'bisa', 'should', 'wajib',
    'mampu', 'able', 'perlu', 'need', 'will', 'akan',
]


def check_ambiguity(text):
    text_lower = text.lower()
    found = [w for w in AMBIGUOUS_WORDS if re.search(r'\b' + w + r'\b', text_lower)]
    return found


def check_measurability(text):
    text_lower = text.lower()
    return any(re.search(p, text_lower) for p in MEASURABLE_PATTERNS)


def check_completeness(text):
    text_lower = text.lower()
    has_actor = any(a in text_lower for a in ACTOR_KEYWORDS)
    has_action = any(a in text_lower for a in ACTION_KEYWORDS)
    word_count = len(text.split())
    return has_actor, has_action, word_count


def validate_requirement(req):
    """Validasi satu requirement, return req + info issues"""
    issues = []
    suggestions = []
    text = req['text']

    # 1. Cek ambiguitas
    ambiguous = check_ambiguity(text)
    if ambiguous:
        issues.append({
            'type': 'AMBIGU',
            'message': f"Kata ambigu: {', '.join(ambiguous)}",
            'severity': 'warning'
        })
        suggestions.append(
            f"Ganti '{ambiguous[0]}' dengan ukuran spesifik "
            f"(contoh: '< 2 detik', '≥ 99%', '≤ 100 MB')"
        )

    # 2. NFR harus terukur
    if req.get('type') == 'Non-Functional':
        if not check_measurability(text):
            issues.append({
                'type': 'TIDAK TERUKUR',
                'message': 'Non-Functional Requirement tidak memiliki ukuran spesifik',
                'severity': 'error'
            })
            suggestions.append(
                "Tambahkan ukuran konkret, contoh: "
                "'dalam waktu < 2 detik', 'uptime ≥ 99,5%'"
            )

    # 3. Kelengkapan
    has_actor, has_action, word_count = check_completeness(text)
    if word_count < 6:
        issues.append({
            'type': 'TIDAK LENGKAP',
            'message': 'Requirement terlalu singkat (< 6 kata)',
            'severity': 'error'
        })
        suggestions.append(
            "Lengkapi dengan: siapa (aktor), apa (aksi), bagaimana (kondisi/ukuran)"
        )

    # 4. Testability
    if not has_actor:
        issues.append({
            'type': 'TIDAK TESTABLE',
            'message': 'Tidak ada aktor yang jelas (user, admin, sistem, dll)',
            'severity': 'warning'
        })
    if not has_action:
        issues.append({
            'type': 'TIDAK TESTABLE',
            'message': 'Tidak ada kata aksi yang jelas (harus, dapat, shall, dll)',
            'severity': 'warning'
        })

    # Hitung skor kualitas
    score = 100
    for issue in issues:
        score -= 20 if issue['severity'] == 'error' else 10
    score = max(score, 0)

    return {
        **req,
        'issues': issues,
        'suggestions': suggestions,
        'quality_score': score,
        'is_valid': all(i['severity'] != 'error' for i in issues),
    }


def validate_all(requirements):
    """Validasi seluruh requirement, return (list_validated, avg_score)"""
    validated = [validate_requirement(req) for req in requirements]
    avg_score = (
        round(sum(r['quality_score'] for r in validated) / len(validated), 1)
        if validated else 0
    )
    return validated, avg_score