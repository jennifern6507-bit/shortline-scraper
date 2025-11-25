import io
from pdfminer.high_level import extract_text

def parse_pdf_from_bytes(pdf_bytes):
    try:
        text = extract_text(io.BytesIO(pdf_bytes))
        return text
    except:
        return ""
