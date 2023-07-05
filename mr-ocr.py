import sys
import csv
import pytesseract
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

# Configuración de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Importe de PDF")
        self.setGeometry(100, 100, 400, 300)

        self.button = QPushButton("Importar PDF", self)
        self.button.setGeometry(150, 80, 100, 30)
        self.button.clicked.connect(self.import_pdf)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(50, 120, 300, 150)

        self.resultados = []

    def import_pdf(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Archivos PDF (*.pdf)")
        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()

            self.resultados = []
            for file_name in file_names:
                self.buscar_palabra_pdf(file_name)

            if self.resultados:
                self.text_edit.setPlainText('\n'.join(self.resultados))
                self.guardar_csv()
            else:
                self.text_edit.setPlainText("La palabra ingresada no se encontró en el PDF.")

    def buscar_palabra_pdf(self, pdf_file):
        with open(pdf_file, 'rb') as archivo:
            lector_pdf = PdfReader(archivo)
            num_paginas = len(lector_pdf.pages)

            # Búsqueda del número de factura y del total
            numero_factura = None
            total_factura = None

            for pagina in range(num_paginas):
                contenido_pagina = lector_pdf.pages[pagina].extract_text()

                # Cuidado: es case sensitive
                if numero_factura is None and "Invoice:" in contenido_pagina and total_factura is None and "Total:" in contenido_pagina:
                    numero_factura = self.obtener_siguiente_palabras(contenido_pagina, "Invoice:", 1)
                    total_factura = self.obtener_siguiente_palabras(contenido_pagina, "Total:", 1)
                    self.resultados.append(f"{numero_factura};{total_factura}")
                    # Si se desea saber el nombre del PDF: self.resultados.append(f"{archivo_pdf};{numero_factura};{total_factura}")
                    break
            
            if numero_factura and total_factura:
                print("-")
            else:
                text = obtener_texto(pdf_file)
                self.resultados.append(expresiones_reg(text, pdf_file))
            
            print(pdf_file)

    def obtener_siguiente_palabras(self, texto, palabra_buscada, cantidad_palabras):
        palabras = texto.split()
        indice_palabra_buscada = palabras.index(palabra_buscada)
        indice_fin = min(indice_palabra_buscada + cantidad_palabras + 1, len(palabras))
        palabras_siguientes = palabras[indice_palabra_buscada + 1:indice_fin]
        return ' '.join(palabras_siguientes)

    def guardar_csv(self):
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix("csv")
        file_path, _ = file_dialog.getSaveFileName(self, "Guardar CSV", "", "Archivos CSV (*.csv)")
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for resultado in self.resultados:
                    writer.writerow([resultado])


def obtener_texto(pdf_file):
        images = convert_from_path(pdf_file)
        final_text = ""

        for pg, img in enumerate(images):
            final_text += pytesseract.image_to_string(img)
        
        return final_text

def expresiones_reg(text, pdf_file):
    # Expresión regular para un invoice que comienza con un caracter
    patron_invoice_letra = r'[A-Z]\d{8}'
    coincidencia_invoice_letra = re.search(patron_invoice_letra, text)

    # Expresión regular para un invoice de 9 dígitos
    patron_invoice_numero = r'\d{9}'
    coincidencia_invoice_numero = re.search(patron_invoice_numero, text)

    if coincidencia_invoice_letra:
        invoice_valor = coincidencia_invoice_letra.group()
    elif coincidencia_invoice_numero:
        invoice_valor = coincidencia_invoice_numero.group()
    else:
        invoice_valor = pdf_file

    # Expresión regular para el total
    patron_total = r'Total:\s*([^\s]+)'
    coincidencia_total = re.search(patron_total, text)

    if coincidencia_total:
        total_valor = coincidencia_total.group(1)
    else:
        total_valor = pdf_file

    return invoice_valor + ";" + total_valor


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())