from PySide6.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QTextCharFormat, QColor



class MainActivity(QWidget):
    """A professional, styled calendar widget highlighting today's date."""

    def __init__(self, mainWin):
        super().__init__()
        self.MainWin = mainWin
        self.setWindowTitle("Calendar")
        self.resize(400, 300)

        # Main layout
        self.layout = QVBoxLayout(self)

        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self._apply_styles()
        self._highlight_today()

        self.layout.addWidget(self.calendar)
        bottom_buttons = QHBoxLayout()
        backB = QPushButton("◁")
        homeB = QPushButton("●")
        recentB = QPushButton("■")
        homeB.clicked.connect(self.goHome)
        bottom_buttons.addWidget(backB)
        bottom_buttons.addWidget(homeB)
        bottom_buttons.addWidget(recentB)
        self.layout.addLayout(bottom_buttons)
    def goHome(self):
        self.hide()
        self.MainWin.show()
        
    def goBack(self):
        self.hide()
        self.MainWin.show()
       
    def gotoRecents(self):
        self.close()
        self.MainWin.show()
                
    def _apply_styles(self):
        """Apply custom styling to the calendar."""
        self.calendar.setStyleSheet("""
            QCalendarWidget QWidget {
                background-color: #121212;  /* Dark background */
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #FFFFFF;             /* Text color */
                selection-background-color: #2196F3;  /* Selected date color */
                selection-color: #FFFFFF;
            }
            QCalendarWidget QToolButton {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-weight: bold;
                border-radius: 4px;
            }
            QCalendarWidget QSpinBox {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
        """)

    def _highlight_today(self):
        """Highlight the current date in the calendar."""
        today = QDate.currentDate()
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#FF6F00"))  # Today’s date highlight
        fmt.setForeground(Qt.black)
        fmt.setFontWeight(QFont.Bold)
        self.calendar.setDateTextFormat(today, fmt)

    def Show(self):
        """Show the calendar window."""
        self.show()


