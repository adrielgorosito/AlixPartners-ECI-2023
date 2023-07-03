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

    def import_pdf(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Archivos PDF (*.pdf)")
        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()[0]

            texto_encontrado = self.buscar_dato_pdf(file_name, "Palabra")

            if texto_encontrado:
                texto_encontrado = self.obtener_siguiente_palabras(texto_encontrado, 10)
                self.text_edit.setPlainText(texto_encontrado)
            else:
                self.text_edit.setPlainText("La palabra ingresada no se encontró en el PDF.")

    def buscar_palabra_pdf(self, archivo_pdf, dato_buscado):
        texto_encontrado = ""
        with open(archivo_pdf, 'rb') as archivo:
            lector_pdf = PdfReader(archivo)
            num_paginas = len(lector_pdf.pages)

            for pagina in range(num_paginas):
                contenido_pagina = lector_pdf.pages[pagina].extract_text()
                if dato_buscado in contenido_pagina:
                    texto_encontrado += contenido_pagina

        return texto_encontrado

    def obtener_palabras(self, texto, cantidad_palabras):
        palabras = texto.split()
        indice_fin = min(cantidad_palabras, len(palabras))
        palabras_siguientes = palabras[:indice_fin]
        return ' '.join(palabras_siguientes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())