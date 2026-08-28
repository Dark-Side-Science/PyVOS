from PySide6.QtQml import QQmlApplicationEngine
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication
import PySide6
print(PySide6.__version__)
app = QGuiApplication(sys.argv)


class Camera:
    def __init__(self, on_close=None):
        self.engine = QQmlApplicationEngine()
        self.engine.load("Camera.qml")

        if not self.engine.rootObjects():
            raise RuntimeError("Failed to load Camera.qml")

        self.root = self.engine.rootObjects()[0]
        self.on_close = on_close

        # Handle window close
        self.root.destroyed.connect(self._on_closed)

    def _on_closed(self):
        if self.on_close:
            self.on_close()
            

Camera()
app.exec()