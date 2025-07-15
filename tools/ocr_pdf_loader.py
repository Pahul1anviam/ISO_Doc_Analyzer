from pdf2image import convert_from_path
import pytesseract

# ✅ Manually set Tesseract path (required for Windows users)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def load_pdf_text_with_ocr(pdf_path):
    try:
        pages = convert_from_path(pdf_path, poppler_path=r"C:\poppler\poppler-24.08.0\Library\bin")
    except Exception as e:
        return f"❌ Error while converting PDF to images: {e}"

    all_text = []
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        all_text.append(text)

    return "\n".join(all_text)




