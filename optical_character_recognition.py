import sys
import csv
import pytesseract
import re
import time
from PyQt5.QtWidgets import QLabel, QMessageBox, QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QProgressBar
from PyQt5.QtCore import Qt
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

# Configuración de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR de PDFs")
        self.setGeometry(100, 100, 400, 330)

        self.num_pdfs_label = QLabel("N° de PDFs ingresados: 0", self)
        self.num_pdfs_label.setGeometry(50, 15, 300, 20)

        self.num_analyzed_label = QLabel("PDFs analizados: 0", self)
        self.num_analyzed_label.setGeometry(50, 45, 300, 20)

        self.button = QPushButton("Importar PDF", self)
        self.button.setGeometry(150, 80, 100, 30)
        self.button.clicked.connect(self.import_pdf)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(50, 120, 300, 150)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(50, 280, 300, 20)
        self.progress_bar.setValue(0)
        
        self.resultados = []
        self.num_analyzed = 0
        self.start_time = 0

    def import_pdf(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Archivos PDF (*.pdf)")

        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            self.resultados = []
            num_files = len(file_names)
            self.progress_bar.setMaximum(num_files)
            self.progress_bar.setValue(0)
            self.num_analyzed = 0
            self.num_pdfs_label.setText(f"N° de PDFs ingresados: {num_files}")
            self.num_analyzed_label.setText("PDFs analizados: 0")
            self.start_time = time.time()
            
            for i, file_name in enumerate(file_names, start=1):
                with open(file_name, 'rb') as archivo:
                    text = obtener_texto(file_name)
                    self.resultados.append(expresiones_reg(text, file_name))

                self.num_analyzed += 1
                self.num_analyzed_label.setText(f"PDFs analizados: {self.num_analyzed}")
                self.progress_bar.setValue(i)
                QApplication.processEvents()

            if self.resultados:
                self.text_edit.setPlainText('\n'.join(self.resultados))
                self.guardar_csv()
                elapsed_time = round(time.time() - self.start_time, 2)

                msg_box = QMessageBox()
                msg_box.setWindowTitle("Proceso terminado")
                msg_box.setText(f"Proceso terminado. Tiempo total: {elapsed_time} segundos")
                msg_box.exec_()

                # self.show_message_box(f"Proceso terminado. Tiempo total: {elapsed_time} segundos")
            else:
                self.text_edit.setPlainText("La palabra ingresada no se encontró en ningún PDF.")

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