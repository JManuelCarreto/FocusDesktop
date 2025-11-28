from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from ui.pantallas.pantalla_home import PantallaHome
from ui.pantallas.pantalla_config import PantallaConfig
from ui.pantallas.pantalla_estudio import PantallaEstudio
from ui.pantallas.pantalla_finestudio import PantallaFin
import sys

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FocusDesktop")
        self.setGeometry(100, 100, 800, 600)

        self.session_time = "0:00 min"
        self.pause_count = 0
        self.tasks_completed = 0
        self.session_tasks_summary = f"Tareas completadas: {self.tasks_completed}/15"

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Instancias de pantallas
        self.home = PantallaHome(self)
        self.gestures = PantallaConfig(self)
        self.session = PantallaEstudio(self)
        self.end = PantallaFin(self)

        self.screens = {
            "home":self.home,
            "gestures": self.gestures,
            "session": self.session,
            "end": self.end
        }

        # Agregar pantallas al stack
        for screen in self.screens.values():
            self.stack.addWidget(screen)

        self.stack.setCurrentWidget(self.home)

    def change_screen(self, screen_name):
        if screen_name == "session":
            self.pause_count = 0
            self.tasks_completed = 0

        if screen_name == "end":
            self.end = PantallaFin(self)
            self.screens["end"] = self.end
            self.stack.addWidget(self.end)

        self.stack.setCurrentWidget(self.screens[screen_name])

