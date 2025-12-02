# services/extractors.py
import io
import docx
import fitz
from typing import Tuple

def extract_text_from_bytes(data: bytes, filename: str) -> Tuple[str, str]:
    """
    Extract text from supported file types: txt, pdf, docx
    Returns text content and file type
    """
    filename_l = filename.lower()
    if filename_l.endswith(".txt"):
        return data.decode("utf-8", errors="replace"), "txt"
    elif filename_l.endswith(".pdf"):
        doc = fitz.open(stream=data, filetype="pdf")
        return "\n".join([p.get_text() for p in doc]), "pdf"
    elif filename_l.endswith(".docx"):
        doc = docx.Document(io.BytesIO(data))
        return "\n".join([p.text for p in doc.paragraphs]), "docx"
    else:
        raise ValueError("Unsupported file type")
