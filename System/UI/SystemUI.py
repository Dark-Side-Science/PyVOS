class LockScreen(QWidget):
    
    def __init__(self, stack, lock_enabled=True):
        super().__init__()
        self.stack = stack
        self.stack.setStyleSheet("background-color: black;")
        
        self.setStyleSheet("background-color: black;")
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.entered_pin = ""
        main_layout.setSpacing(30)
        main_layout.setAlignment(Qt.AlignCenter)
        title = QLabel("Enter PIN")
        title.setStyleSheet("color: white; font-size: 22px;")
        title.setAlignment(Qt.AlignCenter)

        # ===== PIN DOTS =====
        self.pin_label = QLabel("○ ○ ○ ○")
        self.pin_label.setStyleSheet(
            "color: white; font-size: 32px; letter-spacing: 10px;"
        )
        self.pin_label.setAlignment(Qt.AlignCenter)

        # ===== KEYPAD =====
        keypad = QGridLayout()
        keypad.setSpacing(15)

        positions = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('⌫', 3, 0), ('0', 3, 1)
        ]

        for text, row, col in positions:
            btn = QPushButton(text)
            btn.setFixedSize(80, 80)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    font-size: 18px;
                    border-radius: 40px;
                    background-color: #222;
                }
                QPushButton:pressed {
                    background-color: #444;
                }
            """)
            btn.clicked.connect(lambda checked, t=text: self.key_pressed(t))
            keypad.addWidget(btn, row, col)

        # ===== ADD TO LAYOUT =====
        main_layout.addWidget(title)
        main_layout.addWidget(self.pin_label)
        main_layout.addLayout(keypad)

    def key_pressed(self, key):
        if key.isdigit() and len(self.entered_pin) < 4:
            self.entered_pin += key

        elif key == '⌫':
            self.entered_pin = self.entered_pin[:-1]        

        self.update_dots()

    def update_dots(self):
        dots = "● " * len(self.entered_pin)
        empty = "○ " * (4 - len(self.entered_pin))
        self.pin_label.setText((dots + empty).strip())
        if len(self.entered_pin) == 4:
            self.check_pin()

    def check_pin(self):
        if self.entered_pin == self.PASSWORD:
            self.stack.close()
            self.home = HomeScreen()
            self.home.StartShowing()
        else:
            self.pin_label.setText("Wrong PIN ❌")
            self.entered_pin = ""

        QTimer.singleShot(1000, self.update_dots)
   
    def StartShowing(self):
        if self.lock_enabled:
            self.show()
        else:
            self.stack.close()
            AM.startActivity(PM.resolveIntent(action="MAIN", category="HOME"))
        


SCREEN_W = 360
SCREEN_H = 640

class WakeScreen(QWidget):
    
    def __init__(self, lock_enabled):
        super().__init__()
        self.stack = QStackedWidget()
#___________________________________
        
        
        
        
        
#____________________________________
        self.SCREEN_W = 360
        self.SCREEN_H = 640
        self.stack.setFixedSize(SCREEN_W, SCREEN_H)
        self.stack.setStyleSheet("background-color: black")
        self.SWIPE_THRESHOLD = 140
        self.start_pos = None
        self.original_y = 0

        self.setFixedSize(self.SCREEN_W, self.SCREEN_H)
        self.setStyleSheet("background-color: black;")
        self.stack.addWidget(self)
        # ---- UI ----
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 40, 24, 24)
        layout.setAlignment(Qt.AlignTop)

        self.clock = QLabel()
        self.clock.setFont(QFont("Roboto", 52, QFont.Light))
        self.clock.setStyleSheet("color: white;")

        hint = QLabel("Swipe up to unlock")
        hint.setStyleSheet("color: rgba(255,255,255,130);")

        layout.addWidget(self.clock)
        layout.addSpacing(8)
        layout.addWidget(hint)

        # ---- Clock Timer ----
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        t = QTime.currentTime()
        self.clock.setText(
            f"{t.toString('hh:mm AP').replace('AM', '').replace('PM', '')} "
            f"<span style='font-size:18px; opacity:0.6;'>"
            f"{t.toString('AP')}</span>"
        )

    # ---- Touch / Mouse ----
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.start_pos = e.globalPosition().toPoint()
            self.original_y = self.y()

    def mouseMoveEvent(self, e):
        if not self.start_pos:
            return

        dy = e.globalPosition().toPoint().y() - self.start_pos.y()

        if dy < 0:  # Only move UP
            self.move(0, self.original_y + dy)

    def mouseReleaseEvent(self, e):
        if not self.start_pos:
            return

        dy = e.globalPosition().toPoint().y() - self.start_pos.y()

        if abs(dy) > self.SWIPE_THRESHOLD:
            self.slide_up()
        else:
            self.slide_back()

        self.start_pos = None

    # ---- Animations ----
    def slide_up(self):
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(260)
        anim.setStartValue(self.pos())
        anim.setEndValue(QPoint(0, -self.SCREEN_H))
        anim.setEasingCurve(QEasingCurve.OutCubic)

        if self.lock_enabled:
            anim.finished.connect(self.show_lock)
        else:
            anim.finished.connect(self.open_home)

        anim.start()
        self.anim = anim

    def open_home(self):
        self.stack.close()
        AM.startActivity(PM.resolveIntent(action="MAIN", category="HOME"))
    
    def show_lock(self):
        self.lock = LockScreen(self.stack)
        self.stack.addWidget(self.lock)
        self.stack.show()
        
    def slide_back(self):
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(220)
        anim.setStartValue(self.pos())
        anim.setEndValue(QPoint(0, 0))
        anim.setEasingCurve(QEasingCurve.OutCubic)

        anim.start()
        self.anim = anim


