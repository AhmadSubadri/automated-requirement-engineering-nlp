# 🚀 Auto-RE-Tools  
**AI-Powered Requirement Engineering Automation**

Auto-RE-Tools adalah tool berbasis AI untuk mengotomatisasi proses *Requirement Engineering* secara end-to-end, mulai dari elicitation hingga menghasilkan dokumen SRS berstandar IEEE 830.

---

## ✨ Features

- 📄 Upload dokumen (PDF, DOCX, TXT) atau input teks
- 🧠 Ekstraksi requirement otomatis (Elicitation)
- 🔍 Klasifikasi FR & NFR (BERT, RoBERTa, DistilBERT)
- ⚖️ Perbandingan hasil antar model (comparison view)
- 🧩 Generate User Stories & Acceptance Criteria
- ✅ Validasi requirement (ambiguity, completeness, testability)
- 📑 Generate dokumen SRS otomatis (LLM)
- 📥 Export ke `.docx`

---

## 🏗️ Project Structure
```bash
automation-re-tools/
├── app.py
├── requirements.txt
├── .env
├── modules/
│ ├── elicitation.py
│ ├── analysis.py
│ ├── specification.py
│ ├── validation.py
│ └── srs_generator.py
└── utils/
├── file_parser.py
└── export.py
```

---

## ⚙️ System Workflow
```bash
INPUT → ELICITATION → ANALYSIS → SPECIFICATION → VALIDATION → SRS OUTPUT
```

---

## 🟩 Step 2 — Elicitation
```bash
**Proses:**
- Ekstraksi requirement dari dokumen menggunakan NLP
- Identifikasi:
  - Aktor
  - Aksi
  - Objek
  - Kondisi

**Output:**
- List requirement (REQ-001, REQ-002, dst)
- Editable (edit, delete, approve)
```
---

## 🟨 Step 3 — Analysis
```bash
**Proses:**
- Klasifikasi:
  - Functional Requirement (FR)
  - Non-Functional Requirement (NFR)
- Sub-kategori NFR (Security, Performance, dll)
- Deteksi:
  - Duplikasi
  - Konflik
- Prioritas (MoSCoW)

**Output:**
- Statistik requirement
- Tabel klasifikasi & prioritas
- Deteksi konflik
```
---

## 🟧 Step 4 — Specification
```bash
**Proses:**
- Generate User Stories
- Generate Acceptance Criteria
- Generate Use Case
- Generate measurable NFR

**Contoh:**
> As a user, I want to log in so that I can access the system securely.
```
---

## 🟥 Step 5 — Validation
```bash
**Proses:**
- Cek ambiguity ("cepat", "mudah", dll)
- Cek completeness
- Cek testability
- Cek consistency

**Output:**
- Skor kualitas requirement
- Rekomendasi perbaikan otomatis
```
---

## 📑 SRS Output (IEEE 830)
```bash
- Introduction
- Overall Description
- Specific Requirements
  - Functional Requirements
  - Non-Functional Requirements
- Appendix
  - Traceability Matrix
  - Glossary
```
---

## 🧠 NLP Models

Tool ini membandingkan 3 model:

- BERT
- RoBERTa
- DistilBERT

---

## 🔄 Development Strategy

### Phase 1 (Current)
- Pretrained model (tanpa fine-tuning)
- Zero-shot / rule-based
- Fokus: sistem berjalan end-to-end

### Phase 2
- Fine-tuning dengan:
  - PROMISE NFR Dataset
  - PURE Dataset
  - Custom dataset

---

## 📊 Dataset

- PROMISE NFR (625 data)
- PURE Dataset (79 dokumen)
- Custom dataset (opsional)

**Split:**
- 70% Training
- 15% Validation
- 15% Testing

---

## 📈 Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score
- Inference Time

---

## 🔀 Model Comparison Flow
INPUT → PREPROCESSING → MODEL (BERT/RoBERTa/DistilBERT)
→ COMPARISON → SELECT BEST → SRS GENERATION


---

## 🛠️ Tech Stack

- **UI**: Streamlit
- **NLP**: HuggingFace Transformers
- **LLM**: Groq / Gemini API
- **Export**: python-docx

---

## ▶️ How to Run

```bash
git clone https://github.com/your-username/auto-re-tools.git
cd auto-re-tools

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```
🔐 Environment Variables
```bash
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
```
🎯 Use Cases
Penelitian S2 Requirement Engineering
Software / System Analyst
AI-based Software Engineering Tools

📌 Notes
Jangan commit folder venv/
Gunakan requirements.txt untuk dependency
Model bisa di-upgrade tanpa ubah UI

🤝 Contribution
Open untuk:

Fine-tuning model
Improve validation logic
UI/UX enhancement
Dataset tambahan


---

## 🔥 Perubahan yang saya lakukan
- Struktur ulang jadi **section-based (GitHub standard)**
- Hapus ASCII berat → diganti clean diagram
- Konsisten bahasa & istilah
- Lebih “portfolio ready”

---

Kalau kamu mau next level:
- Tambahin **badge (Python, license, dll)**
- Tambahin **GIF demo UI**
- Atau bikin **README versi storytelling (buat HR/portfolio)**

Tinggal bilang 👍