from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from ui.pantallas.pantalla_home import PantallaHome
from ui.pantallas.pantalla_estudio import PantallaEstudio
from ui.pantallas.pantalla_config import PantallaConfig

class VentanaMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FocusDesktop")
        self.setMinimumSize(900, 600)

        self.contenedor = QWidget()
        self.layout = QVBoxLayout(self.contenedor)

        self.menu = QHBoxLayout()

        self.b_home = QPushButton("Home")
        self.b_estudio = QPushButton("Estudio")
        self.b_config = QPushButton("Config")

        estilo = """
                    QPushButton {
                        background-color: #e8f1ff;
                        border: 1px solid #bcd4ff;
                        padding: 8px 16px;
                        border-radius: 10px;
                        font-size: 15px;
                    }
                    QPushButton:hover {
                        background-color: #cddfff;
                    }
                    QPushButton:pressed {
                        background-color: #b3d1ff;
                    }
                """
        self.b_home.setStyleSheet(estilo)
        self.b_estudio.setStyleSheet(estilo)
        self.b_config.setStyleSheet(estilo)

        self.menu.addWidget(self.b_home)
        self.menu.addWidget(self.b_estudio)
        self.menu.addWidget(self.b_config)

        self.layout.addLayout(self.menu)

        self.contenedor_pantallas = QVBoxLayout()
        self.layout.addLayout(self.contenedor_pantallas)

        self.pantalla_actual = None
        self.cambiar_pantalla("home")

        self.b_home.clicked.connect(lambda: self.cambiar_pantalla("home"))
        self.b_estudio.clicked.connect(lambda: self.cambiar_pantalla("estudio"))
        self.b_config.clicked.connect(lambda: self.cambiar_pantalla("config"))

        self.setCentralWidget(self.contenedor)

    def cambiar_pantalla(self, nombre):
        if self.pantalla_actual:
            self.contenedor_pantallas.removeWidget(self.pantalla_actual)
            self.pantalla_actual.deleteLater()

        if nombre == "home":
            self.pantalla_actual = PantallaHome()
        elif nombre == "estudio":
            self.pantalla_actual = PantallaEstudio()
        elif nombre == "config":
            self.pantalla_actual = PantallaConfig()

        self.contenedor_pantallas.addWidget(self.pantalla_actual)
