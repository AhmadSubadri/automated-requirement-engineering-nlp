import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def generate_srs(project_info, requirements, specifications):
    """Generate dokumen SRS lengkap menggunakan LLaMA 3.1 70B via Groq"""

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    fr_list  = [r for r in requirements if r.get('type') == 'Functional']
    nfr_list = [r for r in requirements if r.get('type') == 'Non-Functional']

    # Ringkasan requirement (max 25 item agar tidak overflow token)
    req_lines = "\n".join(
        f"- [{r['id']}] ({r.get('type','?')}, {r.get('priority','?')}) {r['text']}"
        for r in requirements[:25]
    )

    # Ringkasan user stories
    story_lines = "\n".join(
        f"- [{s['req_id']}] {s['user_story']}"
        for s in specifications[:20]
        if s.get('type') == 'Functional'
    )

    prompt = f"""Anda adalah Software Requirement Engineer profesional berpengalaman.
Tugas Anda: Buat dokumen SRS (Software Requirements Specification) lengkap dan profesional
mengikuti standar IEEE 830 dalam Bahasa Indonesia.

═══════════════════════════════════════════
INFORMASI PROYEK
═══════════════════════════════════════════
Nama Sistem   : {project_info.get('name', 'Sistem')}
Deskripsi     : {project_info.get('description', '-')}
Domain        : {project_info.get('domain', 'Umum')}
Stakeholder   : {project_info.get('stakeholders', 'Admin, User')}
Total FR      : {len(fr_list)}
Total NFR     : {len(nfr_list)}

═══════════════════════════════════════════
DAFTAR REQUIREMENT
═══════════════════════════════════════════
{req_lines}

═══════════════════════════════════════════
USER STORIES (FR)
═══════════════════════════════════════════
{story_lines}

═══════════════════════════════════════════
INSTRUKSI PENULISAN SRS
═══════════════════════════════════════════
Tulis SRS lengkap dengan TEPAT struktur berikut (gunakan heading markdown):

# 1. Pendahuluan
## 1.1 Tujuan Dokumen
## 1.2 Ruang Lingkup Sistem
## 1.3 Definisi, Akronim, dan Singkatan
## 1.4 Referensi
## 1.5 Gambaran Umum Dokumen

# 2. Deskripsi Umum Sistem
## 2.1 Perspektif Produk
## 2.2 Fungsi Utama Sistem
## 2.3 Karakteristik Pengguna
## 2.4 Batasan Sistem
## 2.5 Asumsi dan Ketergantungan

# 3. Kebutuhan Fungsional
(Jabarkan setiap FR secara detail dengan format: ID, Deskripsi, Input, Proses, Output)

# 4. Kebutuhan Non-Fungsional
(Jabarkan setiap NFR dengan kategori dan ukuran yang terukur)

# 5. Batasan Desain dan Implementasi

# 6. Atribut Kualitas Sistem

Tulis dalam bahasa formal, profesional, dan lengkap. Setiap section minimal 2 paragraf.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.2,
    )

    return response.choices[0].message.content