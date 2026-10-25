import os, json, sys, time
print("\n", os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "\n")
from PySide6.QtWidgets import (
    QWidget, QScrollArea, QGridLayout,
    QPushButton, QVBoxLayout, QMainWindow,
    QSizePolicy, QLabel, QApplication, QMessageBox, QStackedWidget
)
from PySide6.QtCore import Qt, QTimer, QSize, QObject
from PySide6.QtGui import QIcon, QFont
from PySide6.QtGui import QPalette, QBrush, QPixmap
from PySide6.QtCore import (
    Qt, QTimer, QTime,
    QPoint, QPropertyAnimation, QEasingCurve, Signal
)

from .ServiceManager import ServiceManager as SM
from .LockSettingsManager import LockSettingsService




def SystemImagesFile(image_of, app=None):
    
    if image_of == "App_icon" and app is not None:
        return os.path.join(
        os.path.dirname(__file__),
    "apps",
    f"com.pyvos.{app.lower()}",
    "res",
    "ic_launcher",
    app + "_icon.jpg"
        )
        
    elif image_of == "Home_Wallpaper":
        return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
    "sys",
    "wallpaper",
    "wallpaper.jpg"
        )

class AppButton(QPushButton):

    tapped = Signal()
    longPressed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._on_long_press)

        self.long_press_time = 600   # milliseconds
        self.is_long_press = False
        self.press_pos = QPoint()

    def mousePressEvent(self, event):
        self.press_pos = event.position().toPoint()
        self.is_long_press = False
        self.timer.start(self.long_press_time)

    def mouseMoveEvent(self, event):
        # cancel long press if user moves finger too much
        if (event.position().toPoint() - self.press_pos).manhattanLength() > 10:
            self.timer.stop()

    def mouseReleaseEvent(self, event):

        if self.timer.isActive():
            self.timer.stop()

        if not self.is_long_press:
            self.tapped.emit()

    def _on_long_press(self):
        self.is_long_press = True
        self.longPressed.emit()
        

class HomeScreen(QMainWindow):   
    _instance = None
    
    def __init__(self):
        print("super initilising")
        super().__init__()
        print("super initilised")
        self.PM = SM.getService("PackageManager")
        print("got service PM")
        self.lockservice = LockSettingsService()
        print("lock settings service instanced")
        self.setAutoFillBackground(True)
        self.wallpaper_path = SystemImagesFile("Home_Wallpaper")
        print("got wallpaper path")
        self.internet_on = False
        wallpaper = self.wallpaper_path
        self.apply_scaled_background()
        print("applied scaled background")
        self.setWindowTitle("Home")
        self.resize(360, 640)
        
        self.setStyleSheet(f"""
QMainWindow {{
    background-image: url("{wallpaper}");
    background-repeat: no-repeat;
    background-position: center;
}}
""")
        print("style set")
        self.recentApps = {}
        app_position_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "System", "app_positions.json")
        print("app position file loaded")
        with open(app_position_file) as f:
            self.app_positions = json.load(f)
            print("app positions loaded")
        # =========================
        # SCROLL AREA
        # =========================
        self.scroll = QScrollArea()
        self.start_y = 0
        self.panel_height = 300
        self.start_panel_y = -self.panel_height
        self.panel_start_y = -self.panel_height
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)

        self.pages = QWidget()
        self.pages.setAttribute(Qt.WA_TranslucentBackground)
        self.pages.setStyleSheet("background: transparent;")
        self.scroll.setStyleSheet("background: transparent;")
        self.scroll.viewport().setStyleSheet("background: transparent;")

        self.main_layout = QGridLayout(self.pages)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.scroll.setWidget(self.pages)
        # ===== VERTICAL SWIPE =====
        self.last_mouse_y = 0
        self.vertical_drag = False
        self.panel_open = False
        # =========================
        # CENTRAL UI
        # =========================
        central = QWidget()
        self.mainWin = central
        layout = QVBoxLayout(central)
        
        layout.setContentsMargins(0, 0, 0, 0)

        self.status = QLabel("Page: 1")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color:white; background:black; padding:6px;")

        layout.addWidget(self.scroll)
        layout.addWidget(self.status)
        self.setCentralWidget(central)

        # =========================
        # PAGE SYSTEM
        # =========================
        self.page_width = 0
        max_page = max((pos[0] for pos in self.app_positions.values()), default=0)
        self.page_count = max(max_page + 1, (self.PM.NumOfApps() + 15) // 16)
        self.current_page = 0

        self.create_pages()

        # =========================
        # GESTURE SYSTEM
        # =========================
        self.dragging = False
        self.last_mouse_x = 0
        self.velocity = 0

        # =========================
        # PHYSICS TIMER
        # =========================
        self.timer = QTimer()
        self.timer.timeout.connect(self.physics_step)
        self.timer.start(16)
        self.create_top_panel()
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = HomeScreen()
        return cls._instance
        
    def apply_scaled_background(self):
        pix = QPixmap(self.wallpaper_path)

        if pix.isNull():
            return

        scaled = pix.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,   # <-- REAL "cover" mode
            Qt.SmoothTransformation
        )

        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(scaled))
        self.setPalette(palette)   
    # =====================================================
    # PAGE SIZE DETECTION
    # =====================================================
    def showEvent(self, event):
        super().showEvent(event)

        self.page_width = self.scroll.viewport().width()

        for i in range(self.page_count):
            page = self.main_layout.itemAtPosition(0, i).widget()
            page.setFixedWidth(self.page_width)

        self.pages.setMinimumWidth(self.page_count * self.page_width)


    def create_top_panel(self):
        self.top_panel = QWidget(self)
        self.top_panel.setGeometry(0, -300, self.width(), 300)
        self.top_panel.setStyleSheet("""
        QWidget {
            background-color: rgba(20, 20, 20, 240);
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        }
    """)

        layout = QVBoxLayout(self.top_panel)
        self.internet_button = QPushButton("Internet")
        self.power_off = QPushButton("Power off")
        self.power_off.clicked.connect(self.powerOff)
        self.internet_button.clicked.connect(self.toggle_internet)
        self.internet_button.setStyleSheet("background-color:blue; font-size:18px;")
        layout.addWidget(self.power_off)
        layout.addWidget(self.internet_button)
      # =====================================================
    # CREATE PAGES + BUTTONS
    # =====================================================
    def powerOff(self):
        from ..boot.PowerOS import PowerOff

        self.power_screen = PowerOff()
        self.power_screen.showFullScreen()   # or .show()

    # Close HomeScreen AFTER animation (non-blocking)
        QTimer.singleShot(5200, self.shutdown)
        
    def shutdown(self):
        QApplication.quit()
        
    def toggle_internet(self):
        if self.internet_on:
            self.internet_button.setStyleSheet("background-color:blue; font-size:18px;")
        else:
            self.internet_button.setStyleSheet("background-color:gray; font-size:18px;")
        self.internet_on = not self.internet_on
        
    def create_pages(self):
        self.page_layouts = []
        cols = 4
        rows = 4
        apps_per_page = rows * cols
        num = 1
        count = 0
        i = 0
        apps = self.PM.getInstalledPackages()
        
        
            
        for p in range(self.page_count):
            page = QWidget()            
            page.setAttribute(Qt.WA_TranslucentBackground)
            page.setStyleSheet("background: transparent;")
            layout = QGridLayout(page)            
            page_apps = apps
            for i, app in enumerate(page_apps):
                if app in self.app_positions:
                    saved_page, row, col = self.app_positions[app]
                    if saved_page != p:
                        continue
                else:
                    Page = i // apps_per_page
                    if Page != p:
                        continue
                    index = i % apps_per_page
                    row = index // cols
                    col = index % cols
                i += 1
                btn = AppButton()
                app_id = num
                num += 1
                btn.setFixedSize(80, 80)
                btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

                btn.setFont(QFont("Arial", 12, QFont.Bold))

                # ---------- ICON ----------
                
                icon_ = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), self.PM.getPackageInfo(app).icon_path.lstrip("/"))
                
                if os.path.exists(icon_):
                    btn.setIcon(QIcon(icon_))
                    btn.setIconSize(QSize(64, 64))
                    
                else:
                    print("path " + icon_ + " not exists")
                btn.tapped.connect(lambda checked=False, app= app: self.OpenApp(app))

                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #222;
                        color: white;
                        border-radius: 16px;
                    }
                    QPushButton:pressed {
                        background-color: #555;
                    }
                """)
                
                layout.addWidget(btn, row, col,
                                 alignment=Qt.AlignCenter)

            self.main_layout.addWidget(page, 0, p)
            self.page_layouts.append(layout)
            print(self.page_layouts)
            
            

    # =====================================================
    # APP LAUNCH SIMULATION
    # =====================================================
    def OpenApp(self, pkg):
        Activity = SM.getService("ActivityManager")
        pkg_info = self.PM.getPackageInfo(pkg)
        path = pkg_info.sourceDir
        pkg = pkg_info.packageName
        Activity.startActivity(pkg, path)


    def mousePressEvent(self, event):
        self.dragging = True
        self.vertical_drag = False
        self.start_y = event.position().y()
        self.start_panel_y = self.top_panel.y()   # 👈 IMPORTANT
        self.last_mouse_x = event.position().x()
        self.velocity = 0

    def mouseMoveEvent(self, event):
# Block horizontal paging when panel is open
        if self.panel_open and not self.vertical_drag:
            dx = event.position().x() - self.last_mouse_x
            dy = event.position().y() - self.start_y
            if abs(dx) > abs(dy):
                return
        x = event.position().x()
        y = event.position().y()

        dx = x - self.last_mouse_x
        dy = y - self.start_y

        # Lock vertical gesture
        if not self.vertical_drag:
            if (not self.panel_open and self.start_y < 120 and dy > 0) or self.panel_open:
                if abs(dy) > abs(dx):
                    self.vertical_drag = True

        if self.vertical_drag:
            new_y = self.start_panel_y + dy

            if self.panel_open:
                new_y = min(0, max(-self.panel_height, new_y))
            else:
                new_y = max(-self.panel_height, min(0, new_y))

            self.top_panel.move(0, new_y)
            return

        # Horizontal swipe (unchanged)
        bar = self.scroll.horizontalScrollBar()
        bar.setValue(bar.value() - dx)
        self.velocity = dx * 2
        self.last_mouse_x = x
        

    def mouseReleaseEvent(self, event):
        self.dragging = False

        if self.vertical_drag:
            self.vertical_drag = False

            # Decide based on final position
            if not self.panel_open:
                if self.top_panel.y() > -self.panel_height * 0.5:
                    self.open_panel()
                else:
                    self.close_panel()
            else:
                if self.top_panel.y() < -self.panel_height * 0.5:
                    self.close_panel()
                else:
                    self.open_panel()
            return

    # Existing horizontal logic stays the same
        bar = self.scroll.horizontalScrollBar()
        offset = bar.value() - (self.current_page * self.page_width)

        distance_threshold = self.page_width * 0.20
        velocity_threshold = 12

        # ANDROID / iOS HYBRID LOGIC
        if self.velocity < -velocity_threshold or offset > distance_threshold:
            self.current_page += 1
        elif self.velocity > velocity_threshold or offset < -distance_threshold:
            self.current_page -= 1

        self.current_page = max(0, min(self.page_count - 1, self.current_page))

        self.velocity = 0

    def open_panel(self):
        self.panel_open = True
        self.animate_panel(0)

    def close_panel(self):
        self.panel_open = False
        self.animate_panel(-self.panel_height)

    def animate_panel(self, target_y):
        self.panel_anim = QPropertyAnimation(self.top_panel, b"pos", self)
        self.panel_anim.setDuration(280)
        self.panel_anim.setStartValue(self.top_panel.pos())
        self.panel_anim.setEndValue(QPoint(0, target_y))
        self.panel_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.panel_anim.start() #=====================================================
    # FAST SNAP PHYSICS
    # =====================================================
    def physics_step(self):
        if self.dragging:
            return

        bar = self.scroll.horizontalScrollBar()
        target = self.current_page * self.page_width
        diff = target - bar.value()

        if abs(diff) > 1:
            bar.setValue(bar.value() + diff * 0.45)
        else:
            bar.setValue(target)

    # --- status indicator ---
        dots = ""
        for i in range(self.page_count):
            if i == self.current_page:
                dots += "<span style='color:white; font-size:30px;'>•</span> "
            else:
                dots += "<span style='color:gray; font-size:30px;'>•</span> "
        self.status.setText(dots)
        
    def AskUserPermission(text):
        dialog = QMessageBox()
        dialog.setWindowTitle("Permission Manager")
        dialog.setText(text)
        dialog.setIcon(QMessageBox.Question)
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.button(QMessageBox.Yes).setText("Allow")
        dialog.button(QMessageBox.No).setText("Deny")
        user = dialog.exec()
        if user == QMessageBox.Yes:
            return "Allowed"
        else:
            return "Denied"
        
        
    def StartShowing(self):
        self.show()
        

def lock_screen_password():
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "System", "Passwords.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("LOCK_SCREEN_PASSWORD")
    



class PyVOSWindow:

    def __init__(self, package, activity):
        self.package = package
        self.activity = activity
        self.widget = None
        self.visible = False


class ID:
    _counter = 0

    @classmethod
    def generate(cls, prefix="OBJ"):
        cls._counter += 1

        return f"{prefix}_{cls._counter:06d}"


class WindowManagerService:
    _instance = None
    def __init__(self):
        self._WINDOWS = {}
        self._WINDOW_COUNT = 0
        self._WIDGETS = {}
        self._WIDGET_COUNT = 0
        self._COMMANDS = {
            "NEW": {
                "WINDOW": self.AddWindow,
                "PUSHBUTTON": self.AddPushButton,
                "GRIDLAY": self.AddGridLayout,
                "VLAYOUT": self.AddVerticalLayout,
                "LABEL": self.AddLabel
            },

            "BUTTON": {
                "SET_TEXT": self.setText,
                "SET_ICON": self.ButtonSetIcon,
                "SET_ICON_SIZE": self.ButtonSetIconSize,
                "SET_CHECKABLE": self.ButtonSetCheckable,
                "SET_ENABLED": self.ButtonSetEnabled,
                "SET_TOOLTIP": self.ButtonSetTooltip,
                "CHECKABLE": self.ButtonIsCheckable,
                "CHECKED": self.ButtonIsChecked,
                "ENABLED": self.ButtonIsEnabled,
                "TOOLTIP": self.ButtonTooltip
            },

            "GRIDLAY": {
                "ADDWID": self.addWidget,
                "ADDLAY": self.addLayout,
                "SPACING": self.setSpacing,
                "H_SPACING": self.setHorizontalSpacing,
                "V_SPACING": self.setVerticalSpacing,
                "CONTENTS_MARGINS": self.setContentsMargins,
                "RSTRETCH": self.setRowStretch,
                "CSTRETCH": self.setColumnStretch,
                "ROWMH": self.setRowMinimumHeight,
                "COLMW": self.setColumnMinimumWidth,
                "ITEM_AT": self.itemAtPosition,
                "ROW_COUNT": self.rowCount,
                "COL_COUNT": self.columnCount,
                "SET_ALIGNMENT": self.setAlignment,
            }
        }

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = WindowManagerService()
        return cls._instance

    def requestUI(self, request):
        _request = request.split("|")
        if _request[2] == "NEW":
            if _request[4] == "TEXT":
                return self._COMMANDS["NEW"][_request[3]](_request[0], _request[5])
            self._COMMANDS["NEW"][_request[3]](_request[0])
        if _request[2] == "BUTTON_ID":
            self._COMMANDS["BUTTON"][_request[4]](_request[0], _request[3], _request[5:])
        if _request[2] == "GRIDLAY_ID":
            self._COMMANDS["GRIDLAY"][_request[4]](_request[0], _request[3], _request[5:])

    def AddWindow(self, package, *args):
        self._WINDOWS_COUNT += 1
        window = QWidget()
        window_id = f"WINDOW_{self._WINDOWS_COUNT:06d}"
        self.WINDOWS[window_id] = {"package": package, "window": window}
        return window_id

    def AddPushButton(self, package, text):
        self._WIDGET_COUNT += 1
        button = QPushButton()
        widget_id = f"PUSHBUTTON_{self._WIDGET_COUNT:06d}"
        self.WIDGETS[widget_id] = {"package": package, "push_button": button}
        return widget_id

    def AddGridLayout(self, package, *args):
        self._WIDGET_COUNT += 1
        grid = QGridLayout()
        widget_id = f"GRIDLAYOUT_{self._WIDGET_COUNT:06d}"
        self.WIDGETS[widget_id] = {"package": package, "gridlayout": grid}
        return widget_id

    def AddLabel(self, package, *args):
        self._WIDGET_COUNT += 1
        label = QLabel()
        widget_id = f"LABEL_{self._WIDGET_COUNT:06d}"
        self.WIDGETS[widget_id] = {"package": package, "label": label}
        return widget_id

    def AddVerticalLayout(self, package, *args):
        self._WIDGET_COUNT += 1
        vertical = QVBoxLayout()
        widget_id = f"VERTICAL_{self._WIDGET_COUNT:06d}"
        self.WIDGETS[widget_id] = {"package": package, "vertical": vertical}
        return widget_id

    def setText(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return "REQUEST_EXECUTED"
        if widget["package"] != package:
            return "REQUEST_EXECUTED"
        widget["widget"].setText(args[0])
        return "REQUEST_EXECUTED"

    def ButtonSetIcon(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return "REQUEST_EXECUTED"
        if widget["package"] != package:
            return "REQUEST_EXECUTED"
        widget["widget"].setIcon(QIcon(args[0]))
        return "REQUEST_EXECUTED"

    def ButtonSetIconSize(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return "REQUEST_EXECUTED"
        if widget["package"] != package:
            return "REQUEST_EXECUTED"
        widget["widget"].setIconSize(QSize(int(args[0]), int(args[1])))
        return "REQUEST_EXECUTED"

    def ButtonSetCheckable(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return "REQUEST_EXECUTED"
        if widget["package"] != package:
            return "REQUEST_EXECUTED"
        widget["widget"].setCheckable(bool(args[0]))
        return "REQUEST_EXECUTED"

    def ButtonSetEnabled(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return "REQUEST_EXECUTED"
        if widget["package"] != package:
            return "REQUEST_EXECUTED"
        widget["widget"].setEnabled(bool(args[0]))
        return "REQUEST_EXECUTED"

    def ButtonSetTooltip(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return "REQUEST_EXECUTED"
        if widget["package"] != package:
            return "REQUEST_EXECUTED"
        widget["widget"].setToolTip(args[0])
        return "REQUEST_EXECUTED"

    def ButtonIsCheckable(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return None
        if widget["package"] != package:
            return None
        return widget["widget"].isCheckable()

    def ButtonIsChecked(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return None
        if widget["package"] != package:
            return None
        return widget["widget"].isChecked()

    def ButtonIsEnabled(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return None
        if widget["package"] != package:
            return None
        return widget["widget"].isEnabled()

    def ButtonTooltip(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return None
        if widget["package"] != package:
            return None
        return widget["widget"].toolTip()

    def addWidget(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return None
        if widget["package"] != package:
            return None
        _widget = self.WIDGETS.get(int(args[0]))
        widget["widget"].addWidget(_widget)
        return "REQUEST_EXECUTED"

    def addLayout(self, package, id, args):
        widget = self.WIDGETS.get(id)
        if widget is None:
            return None
        if widget["package"] != package:
            return None
        layout = self.WIDGETS.get(int(args[0]))
        widget["widget"].addLayout(layout)
        return "REQUEST_EXECUTED"

'''   def setSpacing(self, package, id, args):
                "SPACING": self.setSpacing,
                "H_SPACING": self.setHorizontalSpacing,
                "V_SPACING": self.setVerticalSpacing,
                "CONTENTS_MARGINS": self.setContentsMargins,
                "RSTRETCH": self.setRowStretch,
                "CSTRETCH": self.setColumnStretch,
                "ROWMH": self.setRowMinimumHeight,
                "COLMW": self.setColumnMinimumWidth,
                "ITEM_AT": self.itemAtPosition,
                "ROW_COUNT": self.rowCount,
                "COL_COUNT": self.columnCount,
                "SET_ALIGNMENT": self.setAlignment,'''