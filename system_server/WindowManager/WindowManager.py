from PySide6.QtWidgets import QWidget

class WindowManager:
    def __init__(self, UIRegistry):
        self._WINDOWS = UIRegistry
        self._WINDOW_COUNT = 0
        self._COMMANDS = {
            "NEW": {
                "WINDOW": self.AddWindow,
            },

            "WINDOW": {
                "SETLAY": self.setLayout,
                "RESIZE": self.resize,
                "SHOW": self.show
            }
        }

    def requestWindow(self, request):
        _request = request.split("|")
        if _request[1] == "NEW":
            try:
                if _request[3] == "TEXT":
                    return self._COMMANDS["NEW"][_request[2]](_request[0], _request[4])
            except: pass
            return self._COMMANDS["NEW"][_request[2]](_request[0])
        if _request[1] == "WINDOW_ID":
            return self._COMMANDS["WINDOW"][_request[3]](_request[0], _request[2], _request[4:])

    def getUIObj(self, package, id):
        return self._WINDOWS.get(package, id)

    def AddWindow(self, package, *args):
        self._WINDOW_COUNT += 1
        window = QWidget()
        window_id = f"WINDOW_{self._WINDOW_COUNT:06d}"
        self._WINDOWS.register(window_id, package, window)
        return window_id

    def resize(self, package, id, args):
        widget = self.getUIObj(package, id)
        if widget is None:
            return None
        widget.resize(int(args[0]), int(args[1]))
        return "REQUEST_EXECUTED"

    def setLayout(self, package, id, args):
        window = self.getUIObj(package, id)
        layout = self.getUIObj(package, args[0])
        if layout is None:
            return None
        window.setLayout(layout)
        return "REQUEST_EXECUTED"

    def show(self, package, id, args):
        window = self.getUIObj(package, id)
        if window is None:
            return None
        window.show()
        return "REQUEST_EXECUTED"
