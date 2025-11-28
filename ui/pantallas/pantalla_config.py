from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class PantallaConfig(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        layout = QVBoxLayout()

        title = QLabel("CONFIGURACIÓN DE GESTOS")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #003366")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addStretch()

        btn_start_pause = QPushButton("🤚🏼 Iniciar / Pausa")
        btn_next_task = QPushButton("👍🏼 Siguiente Tarea")
        btn_task_done = QPushButton("👍🏼👍🏼 Terminar Sesión")

        layout.addWidget(btn_start_pause, alignment=Qt.AlignCenter)
        layout.addWidget(btn_next_task, alignment=Qt.AlignCenter)
        layout.addWidget(btn_task_done, alignment=Qt.AlignCenter)

        layout.addStretch()

        btn_back = QPushButton("Inicio")
        btn_back.clicked.connect(lambda: self.app.change_screen("home"))
        layout.addWidget(btn_back, alignment=Qt.AlignCenter)

        self.setLayout(layout)