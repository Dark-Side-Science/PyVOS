from .WindowManager import WindowManager
from .WidgetManager import WidgetManager
from .LayoutManager import LayoutManager
from .UIRegistry import UIRegistry

class UIEventDispatcher:
    def __init__(self):
        self.UIRegistry = UIRegistry()
        self.WidgetManager = WidgetManager(self.UIRegistry)
        self.LayoutManager = LayoutManager(self.UIRegistry)
        self.WindowManager = WindowManager(self.UIRegistry)

    def dispatch(self, request):
        _request = request.split("|")
        print("EVENT DISPATCHER: ", _request)
        if _request[1] == "NEW":
            if _request[2] == "WINDOW":
                return self.WindowManager.requestWindow(request)
            if _request[2] == "VLAYOUT":
                return self.LayoutManager.requestLayout(request)
            if _request[2] in ["PUSHBUTTON", "LABEL"]:
                return self.WidgetManager.requestWidget(request)
        TYPE = _request[1].split("_")[0]
        if TYPE in ["BUTTON", "LABEL"]:
            return self.WidgetManager.requestWidget(request)
        if TYPE in ["VLAYOUT", "GRIDLAY"]:
            return self.LayoutManager.requestLayout(request)
        if TYPE == "WINDOW":
            return self.WindowManager.requestWindow(request)


