import pytesseract
from pdf2image import convert_from_path

# Configuración de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def obtener_texto(pdf_file):
    images = convert_from_path(pdf_file)
    final_text = ""

    for pg, img in enumerate(images):
        final_text += pytesseract.image_to_string(img)
    
    return final_text

path = 'pdf_test.pdf'
text = obtener_texto(path)

print(text)