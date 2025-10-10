import pytesseract
from PIL import Image
import pdfplumber
from modules.utils import clean_text

def process_image(path):
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return clean_text(text)

def process_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n"
    return clean_text(text)
