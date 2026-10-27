from PySide6.QtWidgets import QPushButton, QLabel

class WidgetManager:

    def __init__(self, UIRegistry):
        self._WIDGETS = UIRegistry
        self._WIDGET_COUNT = 0
        self._COMMANDS = {
            "NEW": {
                "PUSHBUTTON": self.AddPushButton,
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

            "LABEL": {
                "SET_TEXT": self.setText,
            }
        }

    def requestWidget(self, request):
        _request = request.split("|")
        if _request[1] == "NEW":
            try:
                if _request[3] == "TEXT":
                    return self._COMMANDS["NEW"][_request[2]](_request[0], _request[4])
            except: pass
            return self._COMMANDS["NEW"][_request[2]](_request[0])
        if _request[1] == "BUTTON_ID":
            return self._COMMANDS["BUTTON"][_request[3]](_request[0], _request[2], _request[4:])


    def AddPushButton(self, package, text=""):
        self._WIDGET_COUNT += 1
        button = QPushButton()
        widget_id = f"PUSHBUTTON_{self._WIDGET_COUNT:06d}"
        self._WIDGETS.register(widget_id, package, button)
        return widget_id

    def AddLabel(self, package, *args):
        self._WIDGET_COUNT += 1
        label = QLabel(args[0])
        widget_id = f"LABEL_{self._WIDGET_COUNT:06d}"
        self._WIDGETS.register(widget_id, package, label)
        return widget_id

    def getUIObj(self, package, id):
         return self._WIDGETS.get(package, id)

    def setText(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setText(args[0])
        return "REQUEST_EXECUTED"

    def ButtonSetIcon(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setIcon(QIcon(args[0]))
        return "REQUEST_EXECUTED"

    def ButtonSetIconSize(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setIconSize(QSize(int(args[0]), int(args[1])))
        return "REQUEST_EXECUTED"

    def ButtonSetCheckable(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setCheckable(bool(args[0]))
        return "REQUEST_EXECUTED"

    def ButtonSetEnabled(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setEnabled(bool(args[0]))
        return "REQUEST_EXECUTED"

    def ButtonSetTooltip(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setToolTip(args[0])
        return "REQUEST_EXECUTED"

    def ButtonIsCheckable(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        return widget.isCheckable()

    def ButtonIsChecked(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        return widget.isChecked()

    def ButtonIsEnabled(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        return widget.isEnabled()

    def ButtonTooltip(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        return widget.toolTip()

    def addWidget(self, package, id, args):
        widget = self.getUIObj(package, id)
        _widget = self.getUIObj(package, args[0])
        widget.addWidget(_widget)
        return "REQUEST_EXECUTED"

    def resize(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.resize(int(args[0]), int(args[1]))
        return "REQUEST_EXECUTED"

    def setLayout(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        layout = self.getUIObj(package, args[0])
        if layout is None:
            return None
        widget.setLayout(layout)

        return "REQUEST_EXECUTED"

    def show(self, package, id):
        window = self.getUIObj(package, id)
        if window is None:
            return None
        window.show()
        return "REQUEST_EXECUTED"
