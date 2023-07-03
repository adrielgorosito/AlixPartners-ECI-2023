import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Importe de PDF")
        self.setGeometry(100, 100, 400, 200)

        self.button = QPushButton("Importar PDF", self)
        self.button.setGeometry(150, 80, 100, 30)
        self.button.clicked.connect(self.import_pdf)

    def import_pdf(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Archivos PDF (*.pdf)")
        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            for file_name in file_names:
                print("Nombre del pdf:", file_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())