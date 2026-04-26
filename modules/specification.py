def generate_user_story(req):
    """Generate user story dari FR"""
    actor = req.get('actor', 'Pengguna')
    action = req.get('action', 'melakukan proses').lower()
    text = req['text']
    short = text[:80] + ('...' if len(text) > 80 else '')

    story = (
        f"Sebagai {actor}, saya ingin dapat {action} "
        f"sehingga {short}"
    )

    criteria = [
        f"✓ Given {actor.lower()} membuka sistem, "
        f"When melakukan {action}, "
        f"Then sistem merespons dengan benar sesuai kebutuhan.",
        f"✓ Given input tidak valid, "
        f"When {actor.lower()} submit, "
        f"Then sistem menampilkan pesan error yang informatif.",
        f"✓ Given proses berhasil, "
        f"Then sistem menyimpan data dan menampilkan konfirmasi sukses.",
    ]

    return {
        'req_id': req['id'],
        'user_story': story,
        'acceptance_criteria': criteria,
        'type': 'Functional',
        'priority': req.get('priority', 'Should Have'),
    }


NFR_TEMPLATES = {
    'Performance':     "Sistem harus merespons dalam waktu kurang dari 2 detik untuk 95% dari seluruh request pengguna.",
    'Security':        "Sistem harus mengenkripsi semua data sensitif menggunakan standar minimal AES-256 dan HTTPS.",
    'Usability':       "Antarmuka sistem harus dapat digunakan oleh pengguna baru tanpa pelatihan khusus lebih dari 30 menit.",
    'Reliability':     "Sistem harus memiliki tingkat ketersediaan (uptime) minimal 99,5% dalam satu bulan kalender.",
    'Scalability':     "Sistem harus mampu menangani minimal 500 pengguna bersamaan tanpa penurunan performa signifikan.",
    'Maintainability': "Sistem harus dilengkapi dokumentasi teknis dan log aktivitas untuk memudahkan pemeliharaan.",
    'General':         "Sistem harus memenuhi standar kualitas yang ditetapkan dan dapat diandalkan dalam operasional sehari-hari.",
}

NFR_CRITERIA_TEMPLATES = {
    'Performance':     [
        "✓ 95% request direspons dalam < 2 detik pada beban normal.",
        "✓ Sistem tidak mengalami timeout pada operasi standar.",
    ],
    'Security':        [
        "✓ Semua data sensitif dienkripsi saat disimpan dan ditransmisikan.",
        "✓ Akses tidak sah menghasilkan error 401/403 dan dicatat di log.",
    ],
    'Usability':       [
        "✓ Pengguna baru dapat menyelesaikan tugas utama tanpa bantuan.",
        "✓ Tampilan responsif di perangkat desktop dan mobile.",
    ],
    'Reliability':     [
        "✓ Uptime sistem ≥ 99,5% per bulan.",
        "✓ Sistem memiliki mekanisme backup dan recovery data.",
    ],
    'Scalability':     [
        "✓ Sistem mendukung ≥ 500 concurrent users.",
        "✓ Tidak ada degradasi performa signifikan saat beban puncak.",
    ],
    'Maintainability': [
        "✓ Semua aktivitas kritis dicatat dalam log sistem.",
        "✓ Dokumentasi teknis tersedia dan selalu diperbarui.",
    ],
    'General':         [
        "✓ Sistem memenuhi semua kriteria kualitas yang disepakati.",
    ],
}


def generate_nfr_specification(req):
    """Generate spesifikasi untuk NFR"""
    category = req.get('nfr_category', 'General')
    statement = NFR_TEMPLATES.get(category, NFR_TEMPLATES['General'])
    criteria = NFR_CRITERIA_TEMPLATES.get(category, NFR_CRITERIA_TEMPLATES['General'])

    return {
        'req_id': req['id'],
        'user_story': statement,
        'acceptance_criteria': criteria,
        'type': 'Non-Functional',
        'nfr_category': category,
        'priority': req.get('priority', 'Should Have'),
    }


def generate_all_specifications(analyzed_requirements):
    """Generate spesifikasi untuk semua requirement"""
    specs = []
    for req in analyzed_requirements:
        if req.get('type') == 'Functional':
            specs.append(generate_user_story(req))
        else:
            specs.append(generate_nfr_specification(req))
    return specs