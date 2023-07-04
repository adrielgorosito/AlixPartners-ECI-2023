import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit
from PyPDF2 import PdfReader

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

    def buscar_palabra_pdf(self, archivo_pdf):
        with open(archivo_pdf, 'rb') as archivo:
            lector_pdf = PdfReader(archivo)
            num_paginas = len(lector_pdf.pages)

            # Búsqueda del número de factura y del total
            numero_factura = None
            total_factura = None

            for pagina in range(num_paginas):
                contenido_pagina = lector_pdf.pages[pagina].extract_text()

                # Cuidado: es case sensitive
                if numero_factura is None and "Invoice:" in contenido_pagina:
                    numero_factura = self.obtener_siguiente_palabras(contenido_pagina, "Invoice:", 1)

                if total_factura is None and "Total:" in contenido_pagina:
                    total_factura = self.obtener_siguiente_palabras(contenido_pagina, "Total:", 1)

                if numero_factura and total_factura:
                    self.resultados.append(f"{numero_factura};{total_factura}")
                    break
                    # Si se desea saber el nombre del PDF: self.resultados.append(f"{archivo_pdf};{numero_factura};{total_factura}")

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())