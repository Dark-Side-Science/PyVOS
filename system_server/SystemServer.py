import sys

from PySide6.QtWidgets import QApplication

class SystemServer:
    def __init__(self, services, sm):
        self.WM = None
        self._services = services
        self._sm = sm
        
    def start(self):
        app = QApplication(sys.argv)
        self._sm.RegisterServices(self._services)
        self.WM = self._sm.getService("WindowManager")
        try:
            H = self.WM.HomeScreen.instance()
            H.show()
            app.exec()
        except:
            raise
        # instantiate services here
        

        
        
        
class EventLooper():
    
    def __init__(self):
        super().__init__()