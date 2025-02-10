import pytesseract
from pdf2image import convert_from_path

def perform_ocr(pdf_path: str) -> str:
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Perform OCR on each page
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image) + "\n\n"
    
    return text 