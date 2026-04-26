automation-re-tools/
├── app.py                  ← Main Streamlit app
├── requirements.txt        ← Dependencies
├── .env                    ← API Keys
├── modules/
│   ├── elicitation.py      ← Step 2: Ekstraksi requirement
│   ├── analysis.py         ← Step 3: Klasifikasi 3 model
│   ├── specification.py    ← Step 4: Generate user stories
│   ├── validation.py       ← Step 5: Validasi requirement
│   └── srs_generator.py    ← Step 6: Generate SRS via Groq
└── utils/
    ├── file_parser.py      ← Baca PDF/Word/TXT
    └── export.py           ← Export ke .docx


FASE 1 — Gunakan pretrained model langsung (TANPA fine-tune dulu)
         BERT/RoBERTa/DistilBERT sudah bisa klasifikasi teks
         pakai zero-shot atau rule-based dulu
         → Tools JALAN dulu end-to-end

FASE 2 — Fine-tune dengan dataset PROMISE NFR (bisa paralel/besok)
         Tinggal swap model, UI tidak perlu diubah


Dataset Training:
├── PROMISE NFR Dataset    ← 625 labeled requirements (FR/NFR)
├── PURE Dataset           ← 79 RE documents
└── Custom labeled data    ← Anda bisa buat 50-100 data sendiri
                              untuk domain spesifik (nilai lebih!)

Split:
├── 70% Training
├── 15% Validation
└── 15% Testing


🏗️ Arsitektur Alur Sistem yang Disarankan
╔══════════════════════════════════════════════════════════════╗
║                    USER INTERFACE (Web App)                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  STEP 1          STEP 2         STEP 3        STEP 4         ║
║  INPUT      →   ELICITATION →  ANALYSIS  →  SPECIFICATION   ║
║  PROJECT         RESULT         RESULT        RESULT         ║
║                                                              ║
║                                    ↓                         ║
║                              STEP 5                          ║
║                            VALIDATION                        ║
║                              RESULT                          ║
║                                    ↓                         ║
║                              STEP 6                          ║
║                           OUTPUT: SRS                        ║
║                            DOCUMENT                          ║
╚══════════════════════════════════════════════════════════════╝

🟩 STEP 2 — Elicitation (Tampil ke User)
Proses di balik layar:

NLP/AI membaca dokumen input
Mengekstrak kalimat-kalimat yang mengandung kebutuhan
Mengidentifikasi: Aktor, Aksi, Objek, Kondisi

Yang ditampilkan ke user:
┌─────────────────────────────────────────────┐
│         HASIL ELICITATION                   │
├─────────────────────────────────────────────┤
│ Raw Requirement yang Ditemukan: 24 item     │
│                                             │
│ [REQ-001] "Sistem harus bisa login..."      │
│   Aktor: User  |  Aksi: Login               │
│   Sumber: Halaman 2, Paragraf 3             │
│   [✏️ Edit] [🗑️ Hapus] [✅ Approve]          │
│                                             │
│ [REQ-002] "Admin dapat mengelola data..."   │
│   ...                                       │
│                                             │
│ [+ Tambah Manual]  [Approve Semua]          │
└─────────────────────────────────────────────┘

🟨 STEP 3 — Analysis (Tampil ke User)
Proses di balik layar:

Klasifikasi: Functional (FR) vs Non-Functional (NFR)
Sub-klasifikasi NFR: Performance, Security, Usability, dll
Deteksi duplikasi & konflik
Prioritisasi otomatis (MoSCoW)

Yang ditampilkan ke user:
┌─────────────────────────────────────────────────────┐
│              HASIL ANALYSIS                         │
├─────────────────────────────────────────────────────┤
│ 📊 Statistik:                                       │
│   Functional: 18 req  |  Non-Functional: 6 req      │
│   Duplikat ditemukan: 2  |  Konflik: 1              │
│                                                     │
│ ⚠️  KONFLIK TERDETEKSI:                             │
│   REQ-003 vs REQ-011 — Saling bertentangan          │
│   [Lihat Detail] [Resolve]                          │
│                                                     │
│ 📋 Tabel Klasifikasi & Prioritas:                   │
│  ID      | Tipe | Kategori    | Prioritas           │
│  REQ-001 | FR   | Auth        | Must Have           │
│  REQ-002 | FR   | Management  | Should Have         │
│  REQ-005 | NFR  | Security    | Must Have           │
│  [Edit tiap baris secara inline]                    │
└─────────────────────────────────────────────────────┘

🟧 STEP 4 — Specification (Tampil ke User)
Proses di balik layar:

AI generate User Stories untuk setiap FR
AI generate Acceptance Criteria
Generate Use Case deskripsi
Generate NFR statements yang terukur

Yang ditampilkan ke user:
┌──────────────────────────────────────────────────────┐
│              HASIL SPECIFICATION                     │
├──────────────────────────────────────────────────────┤
│ 👤 USER STORIES                                      │
│                                                      │
│ US-001 (dari REQ-001):                               │
│ "As a registered user, I want to log in using        │
│  email and password, so that I can access the        │
│  system securely."                                   │
│                                                      │
│ Acceptance Criteria:                                 │
│  ✓ Given valid credentials → login success           │
│  ✓ Given invalid credentials → error message         │
│  ✓ Given 3x failed → account locked                  │
│                                                      │
│ [✏️ Edit] [Regenerate AI] [✅ Approve]                │
│                                                      │
│ 📊 USE CASE DIAGRAM  [Preview] [Export PNG]          │
└──────────────────────────────────────────────────────┘

🟥 STEP 5 — Validation (Tampil ke User)
Proses di balik layar:

Cek ambiguitas (kata seperti "cepat", "mudah", "beberapa" → harus diukur)
Cek kelengkapan (ada aktor? ada kondisi? ada ukuran?)
Cek testability
Cek konsistensi keseluruhan

Yang ditampilkan ke user:
┌──────────────────────────────────────────────────────┐
│            LAPORAN VALIDASI                          │
├──────────────────────────────────────────────────────┤
│ Skor Kualitas Requirement: 84/100 ✅                 │
│                                                      │
│ ⚠️  ISSUES DITEMUKAN (3):                            │
│                                                      │
│ [AMBIGU] REQ-007:                                    │
│  "Sistem harus merespons dengan cepat"               │
│  Saran: Ganti dengan ukuran spesifik                 │
│  → "Sistem harus merespons dalam < 2 detik"          │
│  [Gunakan Saran] [Edit Manual]                       │
│                                                      │
│ [TIDAK TESTABLE] REQ-012: ...                        │
│ [TIDAK LENGKAP]  REQ-015: ...                        │
│                                                      │
│ [Fix Semua Otomatis] [Review Manual]                 │
└──────────────────────────────────────────────────────┘

Struktur SRS yang di-generate:
SRS DOCUMENT (IEEE 830)
├── 1. Introduction
│   ├── 1.1 Purpose
│   ├── 1.2 Scope
│   ├── 1.3 Definitions & Abbreviations
│   └── 1.4 Overview
├── 2. Overall Description
│   ├── 2.1 Product Perspective
│   ├── 2.2 Product Functions (Summary)
│   ├── 2.3 User Characteristics
│   └── 2.4 Constraints & Assumptions
├── 3. Specific Requirements
│   ├── 3.1 Functional Requirements (per Use Case)
│   ├── 3.2 Non-Functional Requirements
│   └── 3.3 Interface Requirements
└── Appendix
    ├── A. Traceability Matrix
    └── B. Glossary



🏆 Rekomendasi Arsitektur Hybrid
┌─────────────────────────────────────────────────────────────┐
│                    PIPELINE TOOLS ANDA                      │
├──────────────────┬──────────────────────────────────────────┤
│  TAHAP PROSES    │         3 MODEL YANG DIBANDINGKAN        │
│  (Elicitation,   │                                          │
│   Analysis,      │  Model A    │  Model B    │  Model C     │
│   Validation)    │  (trained)  │  (trained)  │  (trained)   │
├──────────────────┴─────────────┴─────────────┴─────────────┤
│                  TAHAP GENERATE SRS OUTPUT                  │
│            → Gunakan 1 LLM Modern saja (Claude/GPT)         │
│              karena ini bukan objek perbandingan            │
└─────────────────────────────────────────────────────────────┘



📊 Apa yang Diukur & Dibandingkan
INPUT SAMA → 3 MODEL BERBEDA → OUTPUT DIBANDINGKAN

Metric Perbandingan:
┌─────────────────────────────────────────────┐
│  1. Accuracy       — % prediksi benar       │
│  2. Precision      — dari yang diprediksi   │
│                      positif, berapa benar  │
│  3. Recall         — dari yang seharusnya   │
│                      positif, berapa ketemu │
│  4. F1-Score       — harmonic mean P&R      │
│  5. Inference Time — kecepatan prediksi     │
└─────────────────────────────────────────────┘


🔄 Alur Lengkap Sistem dengan Strategi Ini

[USER INPUT: Dokumen / Teks]
         ↓
┌────────────────────────┐
│  PRE-PROCESSING        │  ← Sama untuk semua model
│  (tokenisasi, cleaning)│
└────────────┬───────────┘
             ↓
    ┌─────────────────┐
    │  MODEL SELECTOR │  ← User pilih mau pakai model A/B/C
    └────┬────┬────┬──┘       atau jalankan ketiganya sekaligus
         ↓    ↓    ↓
      BERT  RoBERTa  DistilBERT
         ↓    ↓    ↓
    [Hasil Klasifikasi & Ekstraksi masing-masing]
         ↓    ↓    ↓
    ┌─────────────────┐
    │ COMPARISON VIEW │  ← User lihat perbandingan hasil ketiganya
    │  (side by side) │
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │  USER PILIH     │  ← Pilih hasil model terbaik / merge
    │  HASIL TERBAIK  │
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │  LLM MODERN     │  ← Claude API / GPT-4o free tier
    │  GENERATE SRS   │     untuk generate dokumen akhir
    └────────┬────────┘
             ↓
    [OUTPUT: DOKUMEN SRS LENGKAP]