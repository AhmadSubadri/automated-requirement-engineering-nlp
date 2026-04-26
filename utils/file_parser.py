import re

def parse_file(uploaded_file):
    """Parse uploaded file dan return text"""
    text = ""
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == 'txt':
        text = uploaded_file.read().decode('utf-8')

    elif file_type == 'pdf':
        import PyPDF2
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    elif file_type in ['docx', 'doc']:
        import docx
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return clean_text(text)


def clean_text(text):
    """Bersihkan teks dari karakter tidak perlu"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    return text.strip()


def split_sentences(text):
    """Pecah teks menjadi kalimat-kalimat bermakna"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Juga pecah berdasarkan newline & titik koma
    result = []
    for s in sentences:
        sub = re.split(r'[\n;]', s)
        result.extend(sub)
    result = [s.strip() for s in result if len(s.strip()) > 15]
    return result