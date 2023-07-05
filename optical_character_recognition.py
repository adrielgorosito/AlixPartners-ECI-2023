import pytesseract
import re
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

# Expresión regular para un invoice que comienza con un caracter
patron_invoice_letra = r'[A-Z]\d{8}'
coincidencia_invoice_letra = re.search(patron_invoice_letra, text)

# Expresión regular para un invoice de 9 dígitos
patron_invoice_numero = r'\d{9}'
coincidencia_invoice_numero = re.search(patron_invoice_numero, text)

if coincidencia_invoice_letra:
    invoice_valor = coincidencia_invoice_letra.group()
    print("Invoice:", invoice_valor)
elif coincidencia_invoice_numero:
    invoice_valor = coincidencia_invoice_numero.group()
    print("Invoice:", invoice_valor)
else:
    print("No se encontró ningún invoice")

# Expresión regular para el total
patron_total = r'Total:\s*([^\s]+)'
coincidencia_total = re.search(patron_total, text)

if coincidencia_total:
    total_valor = coincidencia_total.group(1)
    print("Total:", total_valor)
else:
    print("No se encontró el total.")