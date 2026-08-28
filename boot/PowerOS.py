from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class PowerOff(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:black;\ncolor:white;")
        self.label = QLabel("AahanOS")
        self.bottom_label = QLabel("powerd by Aahan")
        self.font = QFont()
        self.font.setPointSize(28)
        self.font.setBold(True)
        self.label.setFont(self.font)
        self.layout = QVBoxLayout()
        self.textView = QTextEdit()
        
        self.setLayout(self.layout)
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.bottom_label, alignment=Qt.AlignBottom|Qt.AlignCenter)
