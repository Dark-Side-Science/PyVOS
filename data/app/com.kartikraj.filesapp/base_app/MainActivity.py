import os
import sys
from PySide6.QtWidgets import (
    QWidget, QListWidget, QListWidgetItem,
    QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import FileSystem


DARK_STYLE = """
QWidget {
    background-color: #121212;
    color: #e0e0e0;
    font-family: Segoe UI;
    font-size: 13px;
}

QListWidget {
    background-color: #1e1e1e;
    border-radius: 12px;
    padding: 8px;
}

QListWidget::item {
    padding: 10px;
    border-radius: 8px;
}

QListWidget::item:selected {
    background-color: #2a82da;
    color: white;
}

QTextEdit {
    background-color: #1e1e1e;
    border-radius: 12px;
    padding: 10px;
    font-family: Consolas;
}

QPushButton {
    background-color: #2a2a2a;
    border: none;
    border-radius: 10px;
    padding: 8px 12px;
}

QPushButton:hover {
    background-color: #3a3a3a;
}

QPushButton:pressed {
    background-color: #2a82da;
}

QLabel#PathLabel {
    font-size: 12px;
    color: #aaaaaa;
}
"""


class MainActivity(QWidget):
    def __init__(self, MainWin):
        super().__init__()
        self.MainWin = MainWin
        self.setStyleSheet(DARK_STYLE)
        self.FS = FileSystem(self, "INTERNAL")
        self.VROOT = "/storage/emulated/0/"
        self.setWindowTitle("Explorer")
        self.resize(950, 550)
        self.ROOT_DIR = self.FS.return_path() #This returns /storage/emulated/0/PyVOS/storage/emulated/0/
        self.current_path = self.ROOT_DIR
        self.history = []

        main = QVBoxLayout(self)
        main.setSpacing(12)
        main.setContentsMargins(12, 12, 12, 12)

        # 🔹 Toolbar
        bar = QHBoxLayout()
        bar.setSpacing(10)

        self.back = QPushButton("⬅")
        self.up = QPushButton("⬆")
        self.refresh = QPushButton("⟳")

        for b in (self.back, self.up, self.refresh):
            b.setFixedSize(40, 40)

        self.path = QLabel()
        self.path.setObjectName("PathLabel")
        self.path.setTextInteractionFlags(Qt.TextSelectableByMouse)

        bar.addWidget(self.back)
        bar.addWidget(self.up)
        bar.addWidget(self.refresh)
        bar.addWidget(self.path)
        bar.addStretch()

        main.addLayout(bar)

        # 🔹 Content
        body = QHBoxLayout()
        body.setSpacing(12)

        self.list = QListWidget()
        self.list.setMinimumWidth(320)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)

        body.addWidget(self.list, 1)

        main.addLayout(body)
        # 🔹 Signals        
        self.list.itemDoubleClicked.connect(self.open_item)
        self.back.clicked.connect(self.go_back)
        self.up.clicked.connect(self.go_up)
        self.refresh.clicked.connect(self.refresh_view)
        bottom_buttons = QHBoxLayout()
        backB = QPushButton("◁")
        homeB = QPushButton("●")
        recentB = QPushButton("■")
        homeB.clicked.connect(self.goHome)
        bottom_buttons.addWidget(backB)
        bottom_buttons.addWidget(homeB)
        bottom_buttons.addWidget(recentB)
        main.addLayout(bottom_buttons)
        self.load(self.current_path)
      
    def goHome(self):
        self.hide()
        self.MainWin.show()
        
    def goBack(self):
        self.hide()
        self.MainWin.show()
       
    def gotoRecents(self):
        self.close()
        self.MainWin.show()
        
    def to_virtual_path(self, real_path):
        rel = os.path.relpath(real_path, self.ROOT_DIR)
        if rel == ".":
            return self.VROOT
        return os.path.join(self.VROOT, rel)
    
    def load(self, path):
      #  path = os.path.abspath(path)
        # 🔒 BLOCK escape
        root = os.path.realpath(self.ROOT_DIR)
        path = os.path.realpath(path)

        if os.path.commonpath([path, root]) != root:            
            return

        self.list.clear()
        self.preview.clear()

        if not self.history or self.history[-1] != path:
            self.history.append(path)

        self.current_path = path
        self.path.setText(self.to_virtual_path(path))

        try:
            items = os.listdir(path)
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))

            for name in items:
                full = os.path.join(path, name)

                item = QListWidgetItem()
                item.setText(("📁 " if os.path.isdir(full) else "📄 ") + name)
                item.setData(Qt.UserRole, full)

                self.list.addItem(item)

        except PermissionError:
            QMessageBox.critical(
        self,
        "Permission denied",
        f"System access denied"
    )

    def open_item(self, item):
        path = item.data(Qt.UserRole)
        if os.path.isdir(path):
     #       if os.path.
            self.load(path)
        else:
            self.open_file(path)


    def open_file(self, path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                self.preview.setText(f.read())
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    
    
    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.load(self.history.pop())

    def go_up(self):
        parent = os.path.dirname(self.current_path)
        if parent and parent != self.current_path:
            self.load(parent)
    def Show(self):
        self.show()
        
    def refresh_view(self):
        self.load(self.current_path)

