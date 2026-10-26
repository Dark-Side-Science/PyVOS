class WindowManagerService:
    _instance = None
    def __init__(self):
        self._WIDGETS = {}
        self._WIDGET_COUNT = 0
        self._COMMANDS = {
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
            }
        }

    def AddPushButton(self, package, text=""):
        self._WIDGET_COUNT += 1
        button = QPushButton()
        widget_id = f"PUSHBUTTON_{self._WIDGET_COUNT:06d}"
        self._WIDGETS[widget_id] = {"package": package, "widget": button}
        return widget_id

    def AddLabel(self, package, *args):
        self._WIDGET_COUNT += 1
        label = QLabel(args[0])
        widget_id = f"LABEL_{self._WIDGET_COUNT:06d}"
        self._WIDGETS[widget_id] = {"package": package, "widget": label}
        return widget_id

    def getWidget(self, package, id):
        widget = self._WIDGETS.get(id)
        win = False
        if widget is None:
            widget = self._WINDOWS.get(id)
            if widget is None:
                return None
            win = True
        if widget["package"] != package:
            return None
        if win:
            return widget["window"]
        return widget["widget"]

    def setText(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        widget.setText(args[0])
        return "REQUEST_EXECUTED"

    def ButtonSetIcon(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        widget.setIcon(QIcon(args[0]))
        return "REQUEST_EXECUTED"

    def ButtonSetIconSize(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        widget.setIconSize(QSize(int(args[0]), int(args[1])))
        return "REQUEST_EXECUTED"

    def ButtonSetCheckable(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        widget.setCheckable(bool(args[0]))
        return "REQUEST_EXECUTED"

    def ButtonSetEnabled(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        widget.setEnabled(bool(args[0]))
        return "REQUEST_EXECUTED"

    def ButtonSetTooltip(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        widget.setToolTip(args[0])
        return "REQUEST_EXECUTED"

    def ButtonIsCheckable(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        return widget.isCheckable()

    def ButtonIsChecked(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        return widget.isChecked()

    def ButtonIsEnabled(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        return widget.isEnabled()

    def ButtonTooltip(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        return widget.toolTip()

    def addWidget(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        _widget = self.getWidget(package, args[0])
        widget.addWidget(_widget)
        return "REQUEST_EXECUTED"

    def resize(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        widget.resize(int(args[0]), int(args[1]))
        return "REQUEST_EXECUTED"
    
    def setLayout(self, package, id, args):
        widget = self.getWidget(package, id)
        if widget is None:
            return None
        layout = self.getWidget(package, args[0])
        if layout is None:
            return None
        widget.setLayout(layout)

        return "REQUEST_EXECUTED"