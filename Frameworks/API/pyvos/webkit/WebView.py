import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView


class :
    def __init__(self):
        super().__init__()
        # Browser engine
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        back = toolbar.addAction("←")
        forward = toolbar.addAction("→")
        reload = toolbar.addAction("⟳")

        back.triggered.connect(self.browser.back)
        forward.triggered.connect(self.browser.forward)
        reload.triggered.connect(self.browser.reload)

        # Address bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL...")
        toolbar.addWidget(self.url_bar)

        self.url_bar.returnPressed.connect(self.load_url)

        self.browser.urlChanged.connect(
            lambda url: self.url_bar.setText(url.toString())
        )

        # Start page
        self.browser.setUrl(QUrl("https://www.youtube.com"))

    def load_url(self):
        text = self.url_bar.text().strip()

        if not text.startswith(("http://", "https://")):
            text = "https://" + text

        self.browser.setUrl(QUrl(text))


app = QApplication(sys.argv)

window = Browser()
window.show()

sys.exit(app.exec())