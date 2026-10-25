import sys
import math

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QApplication, QWidget


class ShutdownScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shutting down")
        self.setStyleSheet("background-color: black;")

        self.angle = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(80)

    def animate(self):
        self.angle = (self.angle + 1) % 12
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() // 2
        cy = self.height() // 2 - 40

        radius = 35
        dot_radius = 4
        dot_count = 12

        for i in range(dot_count):
            angle = math.radians((360 / dot_count) * i)

            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius

            distance = (i - self.angle) % dot_count
            brightness = max(40, 255 - distance * 22)

            painter.setBrush(QColor(brightness, brightness, brightness))
            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                int(x - dot_radius),
                int(y - dot_radius),
                dot_radius * 2,
                dot_radius * 2
            )

        painter.setPen(Qt.white)

        font = painter.font()
        font.setPointSize(18)
        painter.setFont(font)

        painter.drawText(
            0,
            cy + 80,
            self.width(),
            50,
            Qt.AlignCenter,
            "Shutting down..."
        )


app = QApplication(sys.argv)

window = ShutdownScreen()
window.resize(800, 500)
window.show()

sys.exit(app.exec())