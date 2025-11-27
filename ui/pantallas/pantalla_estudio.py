from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PantallaEstudio(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Pantalla Estudio"))
        self.setLayout(layout)
