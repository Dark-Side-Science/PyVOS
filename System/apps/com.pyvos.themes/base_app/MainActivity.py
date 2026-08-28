import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QGridLayout, QVBoxLayout, QHBoxLayout,
    QScrollArea, QStackedWidget
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "res")
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")


class ImageItem(QLabel):
    def __init__(self, path, on_click):
        super().__init__()
        self.path = path
        self.on_click = on_click

        pix = QPixmap(path)
        self.setPixmap(
            pix.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(220, 220)
        self.setStyleSheet("border:1px solid #444;")

    def mousePressEvent(self, event):
        self.on_click(self.path)


class GridPage(QWidget):
    def __init__(self, open_preview):
        super().__init__()
        self.open_preview = open_preview

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(10)

        images = [
            os.path.join(IMAGE_DIR, f)
            for f in os.listdir(IMAGE_DIR)
            if f.lower().endswith(IMAGE_EXTS)
        ]

        row = col = 0
        for img in images:
            item = ImageItem(img, self.open_preview)
            grid.addWidget(item, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        scroll.setWidget(container)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


class PreviewPage(QWidget):
    def __init__(self, go_back):
        super().__init__()
        self.go_back = go_back
        self.current_path = None
        self.original_pix = None   # ✅ store original

        self.image = QLabel(alignment=Qt.AlignCenter)

        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(self.go_back)

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_image)

        top = QHBoxLayout()
        top.addWidget(back_btn)
        top.addStretch()

        bottom = QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(apply_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.image, 1)
        layout.addLayout(bottom)

    def show_image(self, path):
        self.current_path = path
        self.original_pix = QPixmap(path)   # ✅ load once
        self._update_pixmap()

    def resizeEvent(self, event):
        self._update_pixmap()

    def _update_pixmap(self):
        if not self.original_pix:
            return

        self.image.setPixmap(
            self.original_pix.scaled(
                self.image.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    def apply_image(self):
        print("Applied:", self.current_path)

class MainActivity(QWidget):
    def __init__(self, MainWin):
        super().__init__()
        self.setWindowTitle("Themes App")
        self.resize(480, 800)
        self.MainWin = MainWin
        self.stack = QStackedWidget()

        self.grid = GridPage(self.open_preview)
        self.preview = PreviewPage(self.go_back)

        self.stack.addWidget(self.grid)
        self.stack.addWidget(self.preview)
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)
        bottom_buttons = QHBoxLayout()
        backB = QPushButton("◁")
        homeB = QPushButton("●")
        recentB = QPushButton("■")
        homeB.clicked.connect(self.goHome)
        bottom_buttons.addWidget(backB)
        bottom_buttons.addWidget(homeB)
        bottom_buttons.addWidget(recentB)
        layout.addLayout(bottom_buttons)
    
    def goHome(self):
        self.hide()
        self.MainWin.show()
        
    def goBack(self):
        self.hide()
        self.MainWin.show()
       
    def gotoRecents(self):
        self.close()
        self.MainWin.show()

        
    def Show(self):
        self.show()
        
    def open_preview(self, path):
        self.preview.show_image(path)
        self.stack.setCurrentWidget(self.preview)

    def go_back(self):
        self.stack.setCurrentWidget(self.grid)


