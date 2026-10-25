from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView


class WebViewer(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.browser.back
        self.browser.forward
        self.browser.reload

        self.browser.urlChanged.connect(
            lambda url: self.url_bar.setText(url.toString())
        )

        # Start page
        self.browser.setUrl(QUrl("https://www.google.com"))

    def load_url(self):
        text = self.url_bar.text().strip()

        if not text.startswith(("http://", "https://")):
            text = "https://" + text

        self.browser.setUrl(QUrl(text))

    def back(self):