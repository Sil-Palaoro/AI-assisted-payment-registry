#Pdf parser service
import io

import pdfplumber
import pytesseract
from PIL import Image

from config.settings import TESSERACT_CMD


def extract_text_from_pdf(pdf_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
    text = pytesseract.image_to_string(image, lang="spa")  # español
    return text

def extract_text_from_email(msg):
    extracted_texts = []

    for part in msg.walk():
        content_type = part.get_content_type()
        content_disposition = part.get("Content-Disposition", "")
        filename = part.get_filename()

        if part.get_content_maintype() == 'multipart':
            continue

        payload = part.get_payload(decode=True)
        if not payload:
            continue

        # PDF adjunto
        if "application/pdf" in content_type or (filename and filename.lower().endswith(".pdf")):
            try:
                text = extract_text_from_pdf(payload)
                extracted_texts.append(text)
            except Exception as e:
                print(f"Error procesando PDF: {e}")

        # 🖼️ Imagen adjunta o embebida
        elif "image" in content_type:
            try:
                text = extract_text_from_image(payload)
                extracted_texts.append(text)
            except Exception as e:
                print(f"Error procesando imagen: {e}")
    
    return "\n".join(extracted_texts)
