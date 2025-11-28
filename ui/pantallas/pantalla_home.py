from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class PantallaHome(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Título
        title = QLabel("FOCUS Desktop")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #003366;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(30)

        btn_start = QPushButton("+ Iniciar Sesión de Estudio")
        btn_start.setFixedWidth(250)
        btn_start.clicked.connect(lambda: self.app.change_screen("session"))
        layout.addWidget(btn_start, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(50)

        btn_gestures = QPushButton("Ver Gestos")
        btn_gestures.setFixedWidth(150)
        btn_gestures.clicked.connect(lambda: self.app.change_screen("gestures"))

        btn_last = QPushButton("Última Sesión")
        btn_last.setFixedWidth(150)
        btn_last.clicked.connect(lambda: self.app.change_screen("end"))

        bottom_layout.addWidget(btn_gestures)
        bottom_layout.addWidget(btn_last)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)