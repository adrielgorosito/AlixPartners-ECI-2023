import fitz
import os
import random

def es_imagen_escaneada(pdf_file):
    doc = fitz.open(pdf_file)

    for page in doc:
        image_blocks = page.get_images()
        
        if image_blocks:
            return True

    return False

folder_path = r"\AlixPartners ECI 2023\Datos\Todos"
pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

num_imagen_escaneada = 0
num_texto_plano = 0
pdfs_texto_plano = []

for i, pdf_file in enumerate(pdf_files, start=1):
    file_path = os.path.join(folder_path, pdf_file)
    if es_imagen_escaneada(file_path):
        num_imagen_escaneada += 1
        print(f"PDF {i}/{len(pdf_files)} - '{pdf_file}': Imagen escaneada")
    else:
        num_texto_plano += 1
        pdfs_texto_plano.append(pdf_file)


print(f"\nPDFs con imágenes escaneadas: {num_imagen_escaneada}")
print(f"PDFs con texto plano: {num_texto_plano}")

# Verificación: impresión de 10 PDFs aleatorios de texto plano
print("\nAlgunos PDFs texto plano:")
for pdf_file in random.sample(pdfs_texto_plano, k=10):
    print(f"- '{pdf_file}'")