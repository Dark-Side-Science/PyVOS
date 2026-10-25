from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class PowerOff(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:black;\ncolor:white;")
        self.label = QLabel("PyVOS")
        from PySide6.QtGui import QPixmap
        self.b_label = QLabel(self)
        self.b_label.setPixmap(QPixmap("python_logo.png"))
        self.font = QFont()
        self.font.setPointSize(28)
        self.font.setBold(True)
        self.label.setFont(self.font)
        #self.font.setPointSize(10)
        #self.b_label.setFont(self.font)
        self.layout = QVBoxLayout()
        self.textView = QTextEdit()
        
        self.setLayout(self.layout)
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.b_label, alignment=Qt.AlignBottom|Qt.AlignCenter)
