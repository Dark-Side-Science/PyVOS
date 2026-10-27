from PySide6.QtWidgets import QVBoxLayout, QGridLayout

class LayoutManager:

    def __init__(self, UIRegistry):
        self._LAYOUTS = UIRegistry
        self._LAYOUT_COUNT =0
        self._COMMANDS = {
            "NEW": {
                "GRIDLAY": self.AddGridLayout,
                "VLAYOUT": self.AddVerticalLayout
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
            },

            "VLAYOUT": {
                "ADDWID": self.addWidget
            }
        }

    def requestLayout(self, request):
        _request = request.split("|")
        if _request[1] == "NEW":
            try:
                if _request[3] == "TEXT":
                    return self._COMMANDS["NEW"][_request[2]](_request[0], _request[4])
            except: pass
            return self._COMMANDS["NEW"][_request[2]](_request[0])
        if _request[1] == "VLAYOUT_ID":
            return self._COMMANDS["VLAYOUT"][_request[3]](_request[0], _request[2], _request[4:])

    def AddVerticalLayout(self, package, *args):
        self._LAYOUT_COUNT += 1
        vertical = QVBoxLayout()
        layout_id = f"VERTICAL_{self._LAYOUT_COUNT:06d}"
        self._LAYOUTS.register(layout_id, package, vertical)
        return layout_id

    def AddGridLayout(self, package, *args):
        self._LAYOUT_COUNT += 1
        vertical = QVBoxLayout()
        layout_id = f"GRIDLAY_{self._LAYOUT_COUNT:06d}"
        self._LAYOUTS.register(layout_id, package, vertical)
        return layout_id

    def getUIObj(self, package, id):
        return self._LAYOUTS.get(package, id)

    def addWidget(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        _widget = self.getUIObj(package, args[0])
        widget.addWidget(_widget)
        return "REQUEST_EXECUTED"

    def addLayout(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        layout = self.getUIObj(package, args[0])
        widget.addLayout(layout)
        return "REQUEST_EXECUTED"

    def setSpacing(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setSpacing(int(args[0]))
        return "REQUEST_EXECUTED"

    def setHorizontalSpacing(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setHorizontalSpacing(int(args[0]))
        return "REQUEST_EXECUTED"

    def setVerticalSpacing(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setVerticalSpacing(int(args[0]))
        return "REQUEST_EXECUTED"

    def setContentsMargins(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setContentsMargins(int(args[0]), int(args[1]), int(args[2]), int(args[3]))
        return "REQUEST_EXECUTED"

    def setRowStretch(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setRowStretch(int(args[0]), int(args[1]))
        return "REQUEST_EXECUTED"

    def setColumnStretch(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setColumnStretch(int(args[0]), int(args[1]))
        return "REQUEST_EXECUTED"

    def setRowMinimumHeight(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setRowMinimumHeight(int(args[0]), int(args[1]))
        return "REQUEST_EXECUTED"

    def setColumnMinimumWidth(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.setColumnMinimumHeight(int(args[0]), int(args[1]))
        return "REQUEST_EXECUTED"

    def itemAtPosition(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        item = widget.ItemAtPosition(int(args[0]), int(args[1]))
        for item_id, data in self._WIDGETS.items():
            if data["widget"] is item:
                return item_id
        return None

    def rowCount(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        return widget.rowCount()

    def columnCount(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        return widget.columnCount()

    def setAlignment(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        #INCOMPLETE