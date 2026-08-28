import sys, json, os
from pyvos.security.locksettings import LockSettingsService

from PySide6.QtWidgets import (
    QWidget, QListWidget, QStackedWidget,
    QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, 
    QCheckBox, QSlider
)
from PySide6.QtCore import Qt, QTimer


class MainActivity(QWidget):
    def __init__(self, mainWin):
        super().__init__()
        self.MainWin = mainWin
        self.change_password = None
        self.setWindowTitle("Settings")
        self.setFixedSize(360, 640)
        self.setStyleSheet("background-color: #121212; color: white;")
        main_layout = QVBoxLayout()
        center_layout = QHBoxLayout()
        main_layout.addLayout(center_layout)
        self.setLayout(main_layout)
        # ===== Sidebar =====
        self.menu = QListWidget()
        self.menu.addItems(["General", "Display", "Security", "About"])
        self.menu.setFixedWidth(120)
        self.menu.setStyleSheet("""
            QListWidget {
                background: #1e1e1e;
                border: none;
            }
            QListWidget::item {
                padding: 12px;
            }
            QListWidget::item:selected {
                background: #2a82da;
            }
        """)

        # ===== Pages =====
        self.pages = QStackedWidget()
        self.pages.addWidget(self.general_page())
        self.pages.addWidget(self.display_page())
        self.pages.addWidget(self.security_page())
        self.pages.addWidget(self.about_page())


        self.menu.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.menu.setCurrentRow(0)

        center_layout.addWidget(self.menu)
        center_layout.addWidget(self.pages)
        bottom_buttons = QHBoxLayout()
        backB = QPushButton("◁")
        homeB = QPushButton("●")
        recentB = QPushButton("■")
        homeB.clicked.connect(self.goHome)
        bottom_buttons.addWidget(backB)
        bottom_buttons.addWidget(homeB)
        bottom_buttons.addWidget(recentB)
        main_layout.addLayout(bottom_buttons)
    # ===== Pages ====

    def general_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        layout.addWidget(QLabel("General Settings"))

        wifi = QCheckBox("Enable Wi-Fi")
        bluetooth = QCheckBox("Enable Bluetooth")

        layout.addWidget(wifi)
        layout.addWidget(bluetooth)
        layout.addStretch()
        return page
        
    def display_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        layout.addWidget(QLabel("Display"))

        brightness = QLabel("Brightness")
        slider = QSlider(Qt.Horizontal)
        slider.setValue(70)

        dark_mode = QCheckBox("Dark Mode")
        dark_mode.setChecked(True)

        layout.addWidget(brightness)
        layout.addWidget(slider)
        layout.addWidget(dark_mode)
        layout.addStretch()
        return page

    def goHome(self):
        self.hide()
        self.MainWin.show()
        
    def goBack(self):
        self.hide()
        self.MainWin.show()
       
    def gotoRecents(self):
        self.close()
        self.MainWin.show()

    def security_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        layout.addWidget(QLabel("Security"))
        perms = QPushButton("App Permissions")
        lock_change = QPushButton("Change Lock Password")
        lock_change.clicked.connect(self.lock_check)
        lock = QPushButton("Disable Lock Screen")
        lock.clicked.connect(self.lock)
        
        layout.addWidget(lock_change)
        layout.addWidget(lock)
        layout.addWidget(perms)
        layout.addStretch()
        return page

    def Show(self):
        self.show()
            
    def lock(self):
        self.hide()
        check = LockCheck(self, self.on_lock_verified_set)
        check.show()
                
    def lock_check(self):
        self.hide()
        check = LockCheck(self, self.on_lock_verified_change)
        check.show()
        
    def on_lock_verified_set(self, success):
        if success:
            self.lock_set = SetLock(self)
            self.lock_set.show()
            
    def on_lock_verified_change(self, success):
        if success:
            self.change_password = ChangePassword(self)
        else:
            self.show()
            
    def about_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        layout.addWidget(QLabel("""PyVOS – Python Virtual Operating System

Version: 0.1 Alpha
Build: 2026.01.dev

System:
• Architecture: Virtual
• Kernel: PyVOS Core
• Session: Mobile

Hardware (Virtualized):
• CPU: Host CPU (Python Interpreter)
• Memory: Host RAM
• Graphics: Software Rendering
• Storage: Host File System

Software:
• Language: Python 3.x
• UI Framework: PySide6
• App Model: Modular Python Apps
• Multitasking: Simulated

User Interface:
• UI Engine: PyVOS UI Layer
• Window Manager: PyVOS WindowManager
• Theme: Dark
• Rendering: Software

Developed by Kartik Raj
Built for learning and experimentation"""))

        layout.addStretch()
        return page


def lock_screen_password():
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "data", "System", "Passwords.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("LOCK_SCREEN_PASSWORD")
    

class LockCheck(QWidget):
    
    def __init__(self, parent, callback, changing=False, verefing=False):
        super().__init__()
        self.new_pass = ""
        self.changing = changing
        self.verefing = verefing
        self.lock_checked = False
        self.parent = parent
        self.callback = callback
        self.PASSWORD = lock_screen_password()
        self.setStyleSheet("background-color: black;")
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.entered_pin = ""
        main_layout.setSpacing(30)
        main_layout.setAlignment(Qt.AlignCenter)
        if self.changing:
            title = QLabel("Enter New PIN")
        elif self.verefing:
            title = QLabel("Enter Again to Verify")
        else:
            title = QLabel("Enter PIN")
            
        title.setStyleSheet("color: white; font-size: 22px;")
        title.setAlignment(Qt.AlignCenter)
        back = QPushButton("Back")
        back.clicked.connect(self.on_back)
        main_layout.addWidget(back)
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
            ('⌫', 3, 0), ('0', 3, 1), ('OK', 3, 2)
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

        elif key == 'OK':
            self.check_pin()
            return

        self.update_dots()

    def update_dots(self):
        dots = "● " * len(self.entered_pin)
        empty = "○ " * (4 - len(self.entered_pin))
        self.pin_label.setText((dots + empty).strip())
        
    def on_back(self):
        self.callback(False)
        self.close()
        
    
    def New_pass(self, enterd=None, return_=False):
        if enterd is not None:
            self.new_pass = enterd
            return
        if return_:
            return self.new_pass
        
    def check_pin(self):
        if self.changing:
            if len(self.entered_pin) != 4:
                return
            self.New_pass(self.entered_pin)
            self.callback(True)
            self.close()
            return
            
        if self.verefing:
            self.callback(True)
            self.close()
            return

        if self.entered_pin == self.PASSWORD:
            self.lock_checked = True
            self.callback(True)
            self.close()
                                                
        else:
            self.pin_label.setText("Wrong PIN ❌")
            self.entered_pin = ""
        QTimer.singleShot(1000, self.update_dots)
 
   
     
class ChangePassword:
    
    def __init__(self, parent):
        self.parent = parent
        self.new_lock = LockCheck(parent, self.on_enterd, changing=True)
        self.new_lock.show()
        self.new_password = ""
        
    def on_enterd(self, arg):
        self.new_password = self.new_lock.New_pass(return_=True)
        self.new_lock.close()
        self.verify_lock = LockCheck(self.parent, self.on_verified, verefing=True)
        self.verify_lock.show()
        
    def on_verified(self, success):
        if not success:
            self.parent.show()
            return

        if self.verify_lock.entered_pin != self.new_password:
            self.verify_lock.pin_label.setText("PINs do not match ❌")
            self.verify_lock.entered_pin = ""
            QTimer.singleShot(1000, self.verify_lock.update_dots)
            return
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "data", "System", "Passwords.json")
        with open(path, 'r') as f:
            data = json.load(f)
        
        data["LOCK_SCREEN_PASSWORD"] = self.new_password
        
        
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
            self.verify_lock.close()
            self.parent.show()
            


class SetLock(QWidget):
                
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.setStyleSheet("background-color: black; color: white")
        self.setLayout(self.layout)
        self.back = QPushButton('Back')
        self.button = QCheckBox("Dissable lock screen lock")
        password = lock_screen_password()
        if not password or len(password) < 4:
            self.button.setChecked(True)
        else:
            self.button.setChecked(False)
            
        self.layout.addWidget(self.back)
        self.layout.addWidget(self.button)
        self.back.clicked.connect(self.go_back)
        self.button.toggled.connect(self.change_lock_state)
        
    def go_back(self):
        self.parent.show()
        self.close()
        
    def change_lock_state(self, checked):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "data", "System", "Passwords.json")
        if checked:            
            with open(path, 'r') as f:
                data = json.load(f)
                data["LOCK_SCREEN_PASSWORD"] = ""
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
                         
        else:
            with open(path, 'r') as f:
                  data = json.load(f)
                  password = data["LOCK_SCREEN_PASSWORD"]
                  if len(password) < 4:
                      self.change_pass = ChangePassword(self)
