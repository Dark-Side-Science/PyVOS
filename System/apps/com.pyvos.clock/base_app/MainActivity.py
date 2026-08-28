from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget,
    QListView, QApplication, QMessageBox
)
from PySide6.QtCore import (
    QTimer, Qt, QTime, QElapsedTimer,
    QStringListModel
)
from PySide6.QtGui import QFont

class MainActivity(QWidget):
    def __init__(self, mainWin):
        super().__init__()
        self.alert = QMessageBox()
        self.alert.setWindowTitle("Clock")
        self.alert.setIcon(QMessageBox.Warning)
        self.alert.setMinimumSize(420, 220)
        self.alert.setStyleSheet("""
    QLabel {
        font-size: 18px;
    }
    QPushButton {
        font-size: 14px;
        padding: 8px 16px;
    }
""")
        self.MainWin = mainWin
        self.setWindowTitle("Clock")
        self.resize(360, 640)
        self.setStyleSheet("background-color: black; color: white;")

        # =====================
        # STACK
        # =====================
        self.stack = QStackedWidget(self)
        main_layout = QVBoxLayout(self)
        
        bottom_buttons = QHBoxLayout()
        backB = QPushButton("◁")
        homeB = QPushButton("●")
        recentB = QPushButton("■")
        homeB.clicked.connect(self.goHome)
        bottom_buttons.addWidget(backB)
        bottom_buttons.addWidget(homeB)
        bottom_buttons.addWidget(recentB)
        main_layout.addWidget(self.stack)
        main_layout.addLayout(bottom_buttons)


        # =====================
        # CLOCK SCREEN
        # =====================
        self.clockScreen = QWidget()
        clockLayout = QVBoxLayout(self.clockScreen)

        self.clockLabel = QLabel()
        self.clockLabel.setAlignment(Qt.AlignCenter)
        self.clockLabel.setFont(QFont("Arial", 48, QFont.Bold))
        clockLayout.addWidget(self.clockLabel)

        self.clockTimer = QTimer(self)
        self.clockTimer.timeout.connect(self.update_clock)
        self.clockTimer.start(1000)
        self.update_clock()

        swBtn = QPushButton("Stopwatch")
        swBtn.clicked.connect(lambda: self.stack.setCurrentWidget(self.swScreen))
        clockLayout.addWidget(swBtn)

        timerBtn = QPushButton("Timer")
        timerBtn.clicked.connect(lambda: self.stack.setCurrentWidget(self.timerScreen))
        clockLayout.addWidget(timerBtn)

        # =====================
        # STOPWATCH SCREEN
        # =====================
        self.swScreen = QWidget()
        swLayout = QVBoxLayout(self.swScreen)

        self.stopwatchLabel = QLabel("00:00.0")
        self.stopwatchLabel.setAlignment(Qt.AlignCenter)
        self.stopwatchLabel.setFont(QFont("Arial", 36))
        swLayout.addWidget(self.stopwatchLabel)

        sw_btn_layout = QHBoxLayout()
        self.startBtn = QPushButton("Start")
        self.pauseBtn = QPushButton("Pause")
        self.resetBtn = QPushButton("Reset")

        sw_btn_layout.addWidget(self.startBtn)
        sw_btn_layout.addWidget(self.pauseBtn)
        sw_btn_layout.addWidget(self.resetBtn)
        swLayout.addLayout(sw_btn_layout)

        swBack = QPushButton("Back")
        swBack.clicked.connect(lambda: self.stack.setCurrentWidget(self.clockScreen))
        swLayout.addWidget(swBack)

        # =====================
        # TIMER SCREEN (REAL ROLLERS)
        # =====================
        self.timerScreen = QWidget()
        timerLayout = QVBoxLayout(self.timerScreen)

        self.timerLabel = QLabel("00:00")
        self.timerLabel.setAlignment(Qt.AlignCenter)
        self.timerLabel.setFont(QFont("Arial", 36))
        timerLayout.addWidget(self.timerLabel)

        rollerLayout = QHBoxLayout()
        self.hourView = self.create_roller(0, 23)
        self.minView = self.create_roller(0, 59)
        self.secView = self.create_roller(0, 59)

        colon = QLabel(":")
        colon.setFont(QFont("Arial", 28))
        colon.setAlignment(Qt.AlignCenter)
        rollerLayout.addWidget(self.hourView)
        rollerLayout.addWidget(self.minView)
        rollerLayout.addWidget(colon)
        rollerLayout.addWidget(self.secView)

        timerLayout.addLayout(rollerLayout)

        timer_btn_layout = QHBoxLayout()
        self.timerStartBtn = QPushButton("Start")
        self.timerPauseBtn = QPushButton("Pause")
        self.timerResetBtn = QPushButton("Reset")

        timer_btn_layout.addWidget(self.timerStartBtn)
        timer_btn_layout.addWidget(self.timerPauseBtn)
        timer_btn_layout.addWidget(self.timerResetBtn)
        timerLayout.addLayout(timer_btn_layout)

        timerBack = QPushButton("Back")
        timerBack.clicked.connect(lambda: self.stack.setCurrentWidget(self.clockScreen))
        timerLayout.addWidget(timerBack)

        # =====================
        # ADD TO STACK
        # =====================
        self.stack.addWidget(self.clockScreen)
        self.stack.addWidget(self.swScreen)
        self.stack.addWidget(self.timerScreen)
        self.stack.setCurrentWidget(self.clockScreen)

        # =====================
        # STOPWATCH LOGIC
        # =====================
        self.stopwatchTimer = QTimer(self)
        self.stopwatchTimer.timeout.connect(self.update_stopwatch)

        self.elapsedTimer = QElapsedTimer()
        self.paused_ms = 0

        self.startBtn.clicked.connect(self.start_stopwatch)
        self.pauseBtn.clicked.connect(self.pause_stopwatch)
        self.resetBtn.clicked.connect(self.reset_stopwatch)

        # =====================
        # TIMER LOGIC
        # =====================
        self.timerTimer = QTimer(self)
        self.timerTimer.timeout.connect(self.update_timer)
        self.remaining_ms = 0

        self.timerStartBtn.clicked.connect(self.start_timer)
        self.timerPauseBtn.clicked.connect(self.pause_timer)
        self.timerResetBtn.clicked.connect(self.reset_timer)
    
    def goHome(self):
        self.hide()
        self.MainWin.show()
        
    def goBack(self):
        self.hide()
        self.MainWin.show()
       
    def gotoRecents(self):
        self.close()
        self.MainWin.show()
    # =====================
    # ROLLER CREATOR
    # =====================
    def create_roller(self, start, end):
        view = QListView()
        view.setFixedWidth(100)
        view.setFixedHeight(160)
        view.setVerticalScrollMode(QListView.ScrollPerPixel)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setEditTriggers(QListView.NoEditTriggers)
        view.setSpacing(6)

        model = QStringListModel(
            [f"{i:02d}" for i in range(start, end + 1)]
        )
        view.setModel(model)

        view.setFont(QFont("Arial", 26))
        view.setStyleSheet("""
            QListView {
                background: black;
                color: white;
            }
            QListView::item:selected {
                color: #00ffaa;
                font-weight: bold;
            }
        """)

        view.setCurrentIndex(model.index(0))
        view.scrollTo(view.currentIndex(), QListView.PositionAtCenter)

        return view

    # =====================
    # CLOCK
    # =====================
    def update_clock(self):
        self.clockLabel.setText(QTime.currentTime().toString("hh:mm:ss AP"))

    # =====================
    # STOPWATCH
    # =====================
    def start_stopwatch(self):
        if not self.stopwatchTimer.isActive():
            self.elapsedTimer.start()
            self.stopwatchTimer.start(50)

    def pause_stopwatch(self):
        if self.stopwatchTimer.isActive():
            self.paused_ms += self.elapsedTimer.elapsed()
            self.elapsedTimer.invalidate()
            self.stopwatchTimer.stop()

    def reset_stopwatch(self):
        self.stopwatchTimer.stop()
        self.elapsedTimer.invalidate()
        self.paused_ms = 0
        self.stopwatchLabel.setText("00:00.0")

    def update_stopwatch(self):
        t = QTime(0, 0).addMSecs(self.paused_ms + self.elapsedTimer.elapsed())
        self.stopwatchLabel.setText(t.toString("mm:ss.z"))

    # =====================
    # TIMER
    # =====================
    def start_timer(self):
        
        if self.remaining_ms == 0:
            hours = int(self.hourView.currentIndex().data())
            minutes = int(self.minView.currentIndex().data())
            seconds = int(self.secView.currentIndex().data())
            self.remaining_ms = (hours * 3600 + minutes * 60 + seconds) * 1000

        if self.remaining_ms > 0:
            self.timerTimer.start(1000)
            self.update_timer_label()
            
    def pause_timer(self):
        self.timerTimer.stop()

    def reset_timer(self):
        self.timerTimer.stop()
        self.remaining_ms = 0
        self.timerLabel.setText("00:00:00")

    def update_timer(self):
        self.remaining_ms -= 1000
        if self.remaining_ms <= 0:
            self.timerTimer.stop()
            self.timerLabel.setText("00:00:00")
            self.remaining_ms = 0
            self.Alert("Timer went off!")
        else:
            self.update_timer_label()
            
    def Alert(self, msg):
        self.alert.setText(msg)
        self.alert.exec()
        
    def update_timer_label(self):
        t = QTime(0, 0).addMSecs(self.remaining_ms)
        self.timerLabel.setText(t.toString("hh:mm:ss"))
    
    def Show(self):
        self.show()

