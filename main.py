from PySide6.QtWidgets import QApplication
from app.app import App
import sys

if __name__ == "__main__":
    app_qt = QApplication(sys.argv)

    with open("ui/styles.qss", "r") as f:
        app_qt.setStyleSheet(f.read())

    window = App()
    window.show()
    sys.exit(app_qt.exec())