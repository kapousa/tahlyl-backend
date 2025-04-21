import io

from fastapi import UploadFile, HTTPException
from pdfminer.high_level import extract_text


def extract_text_from_pdf(pdf_file: UploadFile):
    """Extracts text from a PDF file."""
    try:
        pdf_content = pdf_file.file.read()
        text_io = io.BytesIO(pdf_content)
        text = extract_text(text_io)  # Corrected Line
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from PDF: {e}")
