from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PantallaHome(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        texto = QLabel("Pantalla Home")
        texto.setStyleSheet("font-size: 30px; color: white;")

        layout.addWidget(texto)
        self.setLayout(layout)

        self.setStyleSheet("background-color: #1e1e1e;")
