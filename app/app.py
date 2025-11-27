from PySide6.QtWidgets import QApplication
from ui.ventana_main import VentanaMain
import sys

class App:
    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.ventana = VentanaMain()

    def run(self):
        self.ventana.show()
        sys.exit(self.qt_app.exec_())
