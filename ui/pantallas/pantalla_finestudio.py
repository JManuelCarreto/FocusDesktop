from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class PantallaFin(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        layout = QVBoxLayout()

        # Título
        title = QLabel("PUNTUACIÓN DE LA SESIÓN")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #003366")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addStretch()

        # Guardamos las etiquetas como atributos de la clase
        self.time_label = QLabel("")
        self.time_label.setStyleSheet("font-size: 20px; color: #007BFF;")
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)

        self.summary_label = QLabel("")
        self.summary_label.setStyleSheet("font-size: 18px; color: #003366; font-weight: bold;")
        self.summary_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.summary_label)

        self.stars_label = QLabel("🎯 Nivel de concentración:")
        self.stars_label.setStyleSheet("font-size: 18px; color: #003366;")
        self.stars_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stars_label)

        layout.addStretch()

        # Botón de regreso
        btn_back = QPushButton("Inicio")
        btn_back.clicked.connect(lambda: self.app.change_screen("home"))
        layout.addWidget(btn_back, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)

        self.time_label.setText(f"⏱ Tiempo de sesión: {self.app.session_time}")

        tasks_completed = self.app.tasks_completed
        pauses = self.app.pause_count

        self.summary_label.setText(f"Tareas completadas: {tasks_completed}/15\nPausas: {pauses}")
        stars = self.calculate_stars(tasks_completed, pauses)
        self.stars_label.setText("⭐" * stars)

    def calculate_stars(self, tasks_completed, pauses):
        stars = 5

        if tasks_completed < 15:
            missing = 15 - tasks_completed
            stars -= (missing // 3)

        stars -= pauses

        if stars < 1:
            stars = 1
        if stars > 5:
            stars = 5

        return stars


