import sys
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
                self.buscar_palabra_pdf(file_name, "Palabra")

            if self.resultados:
                self.text_edit.setPlainText(str(self.resultados))
            else:
                self.text_edit.setPlainText("La palabra ingresada no se encontró en el PDF.")

    def buscar_palabra_pdf(self, archivo_pdf, palabra_a_buscar):
        with open(archivo_pdf, 'rb') as archivo:
            lector_pdf = PdfReader(archivo)
            num_paginas = len(lector_pdf.pages)

            for pagina in range(num_paginas):
                contenido_pagina = lector_pdf.pages[pagina].extract_text()
                if palabra_a_buscar in contenido_pagina:
                    palabras = contenido_pagina.split()
                    indice_fin = min(len(palabras), palabras.index(palabra_a_buscar) + 11)
                    palabras_siguientes = palabras[palabras.index(palabra_a_buscar) + 1:indice_fin]
                    self.resultados.append(' '.join(palabras_siguientes))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())