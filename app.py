import streamlit as st
import pandas as pd
import time

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AutoRE Tools",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    .step-header {
        background: linear-gradient(90deg, #1e3a5f 0%, #2d6a9f 100%);
        color: white; padding: 1rem 1.5rem;
        border-radius: 10px; margin-bottom: 1rem;
    }
    .req-card {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-left: 4px solid #3b82f6;
        padding: 0.8rem 1rem; border-radius: 8px; margin: 0.4rem 0;
    }
    .model-box {
        background: white; border: 1px solid #e2e8f0;
        padding: 1rem; border-radius: 8px; text-align: center;
    }
    .badge-fr  { background:#dbeafe; color:#1e40af; padding:2px 10px; border-radius:12px; font-size:.82em; font-weight:600; }
    .badge-nfr { background:#fce7f3; color:#9d174d; padding:2px 10px; border-radius:12px; font-size:.82em; font-weight:600; }
    .issue-error   { background:#fef2f2; border-left:3px solid #ef4444; padding:.5rem .8rem; margin:.3rem 0; border-radius:4px; }
    .issue-warning { background:#fffbeb; border-left:3px solid #f59e0b; padding:.5rem .8rem; margin:.3rem 0; border-radius:4px; }
    .srs-preview { background:#f8fafc; border:1px solid #e2e8f0; padding:2rem; border-radius:10px; }
    div[data-testid="stProgress"] > div { background-color: #3b82f6 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────
DEFAULTS = {
    'step': 1,
    'project_info': {},
    'raw_text': '',
    'requirements': [],
    'analyzed': [],
    'specifications': [],
    'validated': [],
    'quality_score': 0,
    'srs_content': '',
    'models': {},
    'models_loaded': False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📋 AutoRE Tools")
    st.caption("Automation Requirement Engineering")
    st.divider()

    STEP_LABELS = [
        (1, "📥 Project Setup"),
        (2, "🔍 Elicitation"),
        (3, "🧠 Analysis (3 Model AI)"),
        (4, "📄 Specification"),
        (5, "✅ Validation"),
        (6, "📋 Generate SRS"),
    ]
    current = st.session_state.step
    for num, label in STEP_LABELS:
        if num < current:
            st.success(f"{label} ✓")
        elif num == current:
            st.info(f"**{label}**  ← aktif")
        else:
            st.text(f"   {label}")

    st.divider()
    if st.session_state.project_info:
        st.caption(f"🏗️ **{st.session_state.project_info.get('name','—')}**")
        st.caption(f"🌐 {st.session_state.project_info.get('domain','—')}")
        st.divider()

    if st.button("🔄 Reset Project", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 1 — PROJECT SETUP
# ═══════════════════════════════════════════════════════════════
if st.session_state.step == 1:
    st.markdown('<div class="step-header"><h2>📥 Step 1 — Project Setup & Input</h2>'
                '<p>Masukkan informasi project dan dokumen kebutuhan sistem Anda</p></div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("Informasi Project")
        name = st.text_input("Nama Sistem *", placeholder="contoh: Sistem Informasi Perpustakaan")
        description = st.text_area("Deskripsi Singkat *",
                                   placeholder="Jelaskan tujuan dan fungsi utama sistem...",
                                   height=120)
        domain = st.selectbox("Domain", [
            "Umum / General", "E-Commerce", "Pendidikan", "Kesehatan",
            "Keuangan", "Pemerintahan", "Manufaktur", "Logistik", "Lainnya"
        ])
        stakeholders = st.text_input("Stakeholder Utama",
                                     placeholder="contoh: Admin, User, Manager",
                                     value="Admin, User")

    with col2:
        st.subheader("Input Dokumen Kebutuhan")
        input_method = st.radio("Metode Input", ["📄 Upload File", "✏️ Ketik / Paste Teks"],
                                horizontal=True)
        raw_text = ""

        if input_method == "📄 Upload File":
            uploaded = st.file_uploader("Upload dokumen (PDF, DOCX, TXT)",
                                        type=['pdf', 'docx', 'txt'])
            if uploaded:
                from utils.file_parser import parse_file
                with st.spinner("Membaca dokumen..."):
                    raw_text = parse_file(uploaded)
                st.success(f"✅ Dokumen dibaca — {len(raw_text):,} karakter")
                with st.expander("Preview teks (500 karakter pertama)"):
                    st.text(raw_text[:500] + ("..." if len(raw_text) > 500 else ""))
        else:
            raw_text = st.text_area(
                "Teks kebutuhan",
                placeholder=(
                    "Contoh:\n"
                    "Sistem harus menyediakan fitur login dengan username dan password.\n"
                    "Admin dapat mengelola data pengguna meliputi tambah, edit, dan hapus.\n"
                    "Sistem harus merespons setiap permintaan dalam waktu kurang dari 2 detik.\n"
                    "Pengguna dapat mengunduh laporan dalam format PDF.\n"
                    "Sistem harus mengenkripsi password menggunakan bcrypt."
                ),
                height=250,
            )

    st.divider()
    if st.button("▶️ Mulai Proses Elicitation", type="primary", use_container_width=True):
        if not name.strip():
            st.error("⚠️ Nama sistem wajib diisi!")
        elif not description.strip():
            st.error("⚠️ Deskripsi sistem wajib diisi!")
        elif not raw_text.strip():
            st.error("⚠️ Input dokumen / teks kebutuhan wajib diisi!")
        else:
            st.session_state.project_info = {
                'name': name, 'description': description,
                'domain': domain, 'stakeholders': stakeholders,
            }
            st.session_state.raw_text = raw_text
            st.session_state.step = 2
            st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 2 — ELICITATION
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    from modules.elicitation import extract_requirements

    st.markdown('<div class="step-header"><h2>🔍 Step 2 — Elicitation</h2>'
                '<p>Sistem mengekstrak kandidat requirement dari dokumen input</p></div>',
                unsafe_allow_html=True)

    if not st.session_state.requirements:
        with st.spinner("🔍 Menganalisis dokumen dan mengekstrak requirement..."):
            reqs = extract_requirements(st.session_state.raw_text)
            st.session_state.requirements = reqs

    reqs = st.session_state.requirements
    approved_count = len([r for r in reqs if r['status'] == 'approved'])
    pending_count  = len([r for r in reqs if r['status'] == 'pending'])

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("📋 Total Ditemukan", len(reqs))
    c2.metric("⏳ Menunggu Review", pending_count)
    c3.metric("✅ Disetujui", approved_count)

    st.divider()

    # Bulk actions
    ca, cb, cc = st.columns([1, 1, 3])
    if ca.button("✅ Approve Semua", use_container_width=True):
        for r in st.session_state.requirements:
            r['status'] = 'approved'
        st.rerun()
    if cb.button("➕ Tambah Manual", use_container_width=True):
        n = len(st.session_state.requirements) + 1
        st.session_state.requirements.append({
            'id': f'REQ-{str(n).zfill(3)}',
            'text': 'Tulis requirement di sini...',
            'actor': 'User', 'action': 'Proses',
            'relevance_score': 1, 'source': 'Manual', 'status': 'pending',
        })
        st.rerun()

    # List
    for i, req in enumerate(st.session_state.requirements):
        with st.container():
            col_text, col_status, col_action = st.columns([6, 1, 2])
            with col_text:
                new_text = st.text_input(
                    f"req_{i}", req['text'], key=f"rt_{i}", label_visibility="collapsed"
                )
                st.session_state.requirements[i]['text'] = new_text
                st.caption(
                    f"🆔 `{req['id']}` | 👤 {req['actor']} | "
                    f"⚡ {req['action']} | 📍 {req['source']}"
                )
            with col_status:
                icon = "🟢" if req['status'] == 'approved' else "🟡"
                st.write(f"{icon}")
            with col_action:
                lbl = "✅ Approve" if req['status'] == 'pending' else "↩️ Undo"
                if st.button(lbl, key=f"ap_{i}", use_container_width=True):
                    new_s = 'approved' if req['status'] == 'pending' else 'pending'
                    st.session_state.requirements[i]['status'] = new_s
                    st.rerun()
                if st.button("🗑️ Hapus", key=f"del_{i}", use_container_width=True):
                    st.session_state.requirements.pop(i)
                    st.rerun()
            st.divider()

    approved_now = len([r for r in st.session_state.requirements if r['status'] == 'approved'])
    if st.button(f"▶️ Lanjut ke Analysis ({approved_now} requirement disetujui)",
                 type="primary", use_container_width=True):
        if approved_now == 0:
            st.error("⚠️ Approve minimal 1 requirement terlebih dahulu!")
        else:
            approved_list = [r for r in st.session_state.requirements if r['status'] == 'approved']
            st.session_state.requirements = approved_list
            st.session_state.step = 3
            st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 3 — ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    from modules.analysis import analyze_requirements, load_models

    st.markdown('<div class="step-header"><h2>🧠 Step 3 — Analysis (3 Model AI)</h2>'
                '<p>BERT · RoBERTa · DistilBERT mengklasifikasi requirement secara bersamaan</p></div>',
                unsafe_allow_html=True)

    # Load models sekali saja
    if not st.session_state.models_loaded:
        with st.spinner(
            "⚙️ Loading 3 model AI (BERT, RoBERTa, DistilBERT)...\n"
            "Download pertama kali ±5–15 menit tergantung koneksi. Harap tunggu."
        ):
            models = load_models()
            st.session_state.models = models
            st.session_state.models_loaded = True

        # Status load
        for name, m in st.session_state.models.items():
            if m['status'] == 'loaded':
                st.success(f"✅ {name} berhasil dimuat")
            else:
                st.warning(f"⚠️ {name}: {m['status']} — akan pakai rule-based fallback")

    # Jalankan analisis
    if not st.session_state.analyzed:
        total = len(st.session_state.requirements)
        progress_bar = st.progress(0, text="Memulai analisis...")
        analyzed_temp = []

        for idx, req in enumerate(st.session_state.requirements):
            progress_bar.progress(
                (idx + 1) / total,
                text=f"Menganalisis {req['id']} ({idx+1}/{total})..."
            )
            from modules.analysis import analyze_requirements as _ar
            result = _ar([req], st.session_state.models)
            analyzed_temp.extend(result)

        progress_bar.empty()
        st.session_state.analyzed = analyzed_temp

    analyzed = st.session_state.analyzed

    # Summary metrics
    fr_c  = len([r for r in analyzed if r['type'] == 'Functional'])
    nfr_c = len([r for r in analyzed if r['type'] == 'Non-Functional'])
    cons  = len([r for r in analyzed if r.get('consensus')])
    avg_conf = sum(r['avg_confidence'] for r in analyzed) / len(analyzed)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚙️ Functional",       fr_c)
    c2.metric("🔒 Non-Functional",   nfr_c)
    c3.metric("🤝 Konsensus 3 Model", f"{cons}/{len(analyzed)}")
    c4.metric("📊 Avg Confidence",   f"{avg_conf:.1f}%")

    st.divider()

    # ── Tabel ringkasan ──────────────────────────────────────
    st.subheader("📊 Ringkasan Klasifikasi")
    df_summary = pd.DataFrame([{
        'ID':        r['id'],
        'Requirement': r['text'][:65] + ('...' if len(r['text']) > 65 else ''),
        'BERT':      r['model_results']['BERT']['type'],
        'RoBERTa':   r['model_results']['RoBERTa']['type'],
        'DistilBERT':r['model_results']['DistilBERT']['type'],
        'Final (Voting)': r['type'],
        'Prioritas': r['priority'],
        'Konsensus': '✅' if r['consensus'] else '⚠️',
    } for r in analyzed])
    st.dataframe(df_summary, use_container_width=True)

    st.divider()

    # ── Detail per requirement ───────────────────────────────
    st.subheader("🔬 Detail Perbandingan 3 Model")
    for req in analyzed:
        consensus_icon = "✅ Konsensus" if req['consensus'] else "⚠️ Berbeda Pendapat"
        exp_label = f"{req['id']} — {req['text'][:60]}... | {consensus_icon}"
        with st.expander(exp_label):
            cb, cr, cd = st.columns(3)
            for col, mname in zip([cb, cr, cd], ['BERT', 'RoBERTa', 'DistilBERT']):
                res = req['model_results'][mname]
                with col:
                    badge = "🔵 Functional" if res['type'] == 'Functional' else "🔴 Non-Functional"
                    st.markdown(f"**{mname}**")
                    st.write(badge)
                    st.progress(min(res['confidence'] / 100, 1.0))
                    st.caption(f"Confidence: {res['confidence']}%")
                    st.caption(f"⏱️ {res['inference_time_ms']} ms")
                    st.caption(f"Metode: {res['method']}")

            st.markdown("---")
            ca2, cb2, cc2, cd2 = st.columns(4)
            final_badge = "🔵 Functional" if req['type'] == 'Functional' else "🔴 Non-Functional"
            ca2.markdown(f"**Final:** {final_badge}")
            cb2.markdown(f"**Prioritas:** {req['priority']}")
            cc2.markdown(f"**Kategori NFR:** {req.get('nfr_category', '-')}")
            cd2.markdown(f"**Avg Conf:** {req['avg_confidence']}%")

    st.divider()

    # ── Statistik agregat model ──────────────────────────────
    st.subheader("📈 Statistik Performa 3 Model")
    model_stats = {m: {'agree': 0, 'total': 0, 'times': []} for m in ['BERT', 'RoBERTa', 'DistilBERT']}
    for req in analyzed:
        for mn in ['BERT', 'RoBERTa', 'DistilBERT']:
            res = req['model_results'][mn]
            model_stats[mn]['total'] += 1
            if res['type'] == req['type']:
                model_stats[mn]['agree'] += 1
            model_stats[mn]['times'].append(res['inference_time_ms'])

    stats_rows = []
    for mn, s in model_stats.items():
        agree_pct = round(s['agree'] / s['total'] * 100, 1) if s['total'] else 0
        avg_time  = round(sum(s['times']) / len(s['times']), 1) if s['times'] else 0
        stats_rows.append({
            'Model': mn,
            'Sesuai Voting (%)': f"{agree_pct}%",
            'Avg Inference Time (ms)': avg_time,
        })
    st.dataframe(pd.DataFrame(stats_rows), use_container_width=True)

    if st.button("▶️ Lanjut ke Specification", type="primary", use_container_width=True):
        st.session_state.step = 4
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 4 — SPECIFICATION
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    from modules.specification import generate_all_specifications

    st.markdown('<div class="step-header"><h2>📄 Step 4 — Specification</h2>'
                '<p>Generate User Stories dan Acceptance Criteria dari hasil analisis</p></div>',
                unsafe_allow_html=True)

    if not st.session_state.specifications:
        with st.spinner("📝 Generating specifications..."):
            specs = generate_all_specifications(st.session_state.analyzed)
            st.session_state.specifications = specs

    specs = st.session_state.specifications
    fr_specs  = [s for s in specs if s['type'] == 'Functional']
    nfr_specs = [s for s in specs if s['type'] == 'Non-Functional']

    tab1, tab2 = st.tabs([
        f"⚙️ Functional Requirement ({len(fr_specs)})",
        f"🔒 Non-Functional Requirement ({len(nfr_specs)})",
    ])

    with tab1:
        for s in fr_specs:
            with st.expander(f"{s['req_id']} — {s['user_story'][:65]}..."):
                st.markdown("**👤 User Story:**")
                edited = st.text_area("", s['user_story'], key=f"us_{s['req_id']}",
                                      label_visibility="collapsed", height=80)
                st.markdown("**✅ Acceptance Criteria:**")
                for c in s['acceptance_criteria']:
                    st.write(c)
                st.caption(f"Prioritas: {s['priority']}")

    with tab2:
        for s in nfr_specs:
            with st.expander(f"{s['req_id']} — {s['user_story'][:65]}..."):
                st.markdown("**📐 Spesifikasi NFR:**")
                st.info(s['user_story'])
                st.markdown("**✅ Acceptance Criteria:**")
                for c in s['acceptance_criteria']:
                    st.write(c)
                st.caption(f"Kategori: {s.get('nfr_category','-')} | Prioritas: {s['priority']}")

    if st.button("▶️ Lanjut ke Validation", type="primary", use_container_width=True):
        st.session_state.step = 5
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 5 — VALIDATION
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    from modules.validation import validate_all

    st.markdown('<div class="step-header"><h2>✅ Step 5 — Validation</h2>'
                '<p>Memeriksa kualitas, ambiguitas, kelengkapan, dan testability requirement</p></div>',
                unsafe_allow_html=True)

    if not st.session_state.validated:
        with st.spinner("🔍 Memvalidasi semua requirement..."):
            validated, score = validate_all(st.session_state.analyzed)
            st.session_state.validated  = validated
            st.session_state.quality_score = score

    validated = st.session_state.validated
    score     = st.session_state.quality_score

    # Skor visual
    color = "🟢" if score >= 80 else ("🟡" if score >= 60 else "🔴")
    _, cm, _ = st.columns([1, 2, 1])
    with cm:
        st.markdown(f"<h1 style='text-align:center'>{color}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center'>Skor Kualitas Rata-rata: {score}/100</h2>",
                    unsafe_allow_html=True)
        st.progress(score / 100)

    st.divider()

    valid_c   = len([r for r in validated if r['is_valid']])
    issues_c  = sum(len(r['issues']) for r in validated)
    c1, c2, c3 = st.columns(3)
    c1.metric("✅ Requirement Valid",    valid_c)
    c2.metric("⚠️ Total Issues",         issues_c)
    c3.metric("🔧 Perlu Perbaikan",      len(validated) - valid_c)

    st.divider()

    for req in validated:
        if not req['issues']:
            st.success(f"✅ {req['id']} — {req['text'][:70]}...")
        else:
            with st.expander(f"⚠️ {req['id']} — {req['text'][:60]}... (Skor: {req['quality_score']}/100)"):
                for issue in req['issues']:
                    css = "issue-error" if issue['severity'] == 'error' else "issue-warning"
                    icon = "❌" if issue['severity'] == 'error' else "⚠️"
                    st.markdown(
                        f"<div class='{css}'>{icon} <b>{issue['type']}</b>: {issue['message']}</div>",
                        unsafe_allow_html=True
                    )

                if req['suggestions']:
                    st.markdown("**💡 Saran Perbaikan:**")
                    for sug in req['suggestions']:
                        st.info(f"💡 {sug}")

                new_text = st.text_input(
                    "✏️ Edit requirement:", req['text'], key=f"fix_{req['id']}"
                )
                if new_text != req['text']:
                    for r in st.session_state.analyzed:
                        if r['id'] == req['id']:
                            r['text'] = new_text
                    st.success("Tersimpan! Re-validasi akan dilakukan otomatis.")

    if st.button("▶️ Generate Dokumen SRS", type="primary", use_container_width=True):
        # Reset validated supaya re-validasi dengan teks yang sudah diedit
        st.session_state.validated = []
        st.session_state.step = 6
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 6 — GENERATE SRS
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 6:
    from modules.validation import validate_all
    from modules.srs_generator import generate_srs
    from utils.export import export_to_docx

    st.markdown('<div class="step-header"><h2>📋 Step 6 — Generate SRS Document</h2>'
                '<p>LLaMA 3.1 70B via Groq menyusun dokumen SRS lengkap berstandar IEEE 830</p></div>',
                unsafe_allow_html=True)

    # Re-validasi final jika belum
    if not st.session_state.validated:
        validated, score = validate_all(st.session_state.analyzed)
        st.session_state.validated     = validated
        st.session_state.quality_score = score

    # Generate SRS
    if not st.session_state.srs_content:
        with st.spinner("📝 LLaMA 3.1 70B sedang menyusun dokumen SRS... (30–90 detik)"):
            try:
                srs = generate_srs(
                    st.session_state.project_info,
                    st.session_state.analyzed,
                    st.session_state.specifications,
                )
                st.session_state.srs_content = srs
            except Exception as e:
                st.error(f"❌ Gagal generate SRS: {e}")
                st.info("Pastikan GROQ_API_KEY sudah benar di file `.env`")
                st.stop()

    srs = st.session_state.srs_content

    # Summary
    analyzed = st.session_state.analyzed
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📋 Total Requirement", len(analyzed))
    c2.metric("⚙️ Functional",  len([r for r in analyzed if r['type'] == 'Functional']))
    c3.metric("🔒 Non-Functional", len([r for r in analyzed if r['type'] == 'Non-Functional']))
    c4.metric("⭐ Skor Kualitas", f"{st.session_state.quality_score}/100")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📄 Preview SRS", "📊 Traceability Matrix", "📥 Export"])

    with tab1:
        st.markdown('<div class="srs-preview">', unsafe_allow_html=True)
        st.markdown(srs)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        df_trace = pd.DataFrame([{
            'ID':             r['id'],
            'Requirement':    r['text'][:65] + ('...' if len(r['text']) > 65 else ''),
            'Tipe':           r['type'],
            'Kategori NFR':   r.get('nfr_category', '-'),
            'Prioritas':      r['priority'],
            'Avg Confidence': f"{r['avg_confidence']}%",
            'Skor Kualitas':  r.get('quality_score', '-'),
        } for r in analyzed])
        st.dataframe(df_trace, use_container_width=True, height=400)

    with tab3:
        st.subheader("Export Dokumen SRS")
        col_docx, col_txt = st.columns(2)

        with col_docx:
            docx_buf = export_to_docx(
                st.session_state.project_info,
                st.session_state.analyzed,
                srs,
            )
            fname = st.session_state.project_info.get('name', 'SRS').replace(' ', '_')
            st.download_button(
                "📥 Download SRS (.docx)",
                data=docx_buf,
                file_name=f"SRS_{fname}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

        with col_txt:
            st.download_button(
                "📥 Download SRS (.txt)",
                data=srs,
                file_name=f"SRS_{fname}.txt",
                mime="text/plain",
                use_container_width=True,
            )

    st.divider()
    st.success("🎉 Selesai! Dokumen SRS berhasil di-generate dan siap digunakan.")
    st.balloons()