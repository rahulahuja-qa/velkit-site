import io
from PyPDF2 import PdfReader
from docx import Document

def read_text_from_upload(fs) -> str:
    name = (fs.filename or "").lower()
    data = fs.read()
    fs.stream.seek(0)
    if name.endswith(".pdf"):
        r = PdfReader(io.BytesIO(data))
        return "\n".join((p.extract_text() or "") for p in r.pages)
    if name.endswith(".docx"):
        d = Document(io.BytesIO(data))
        return "\n".join(p.text for p in d.paragraphs)
    try:
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""
