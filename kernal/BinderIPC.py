from system_server.WindowManagerService import WindowManagerService
from ..system_server.ServiceManager import ServiceManager as SM


class IBinder:
    
    def __init__(self):
        self.req = None
        self.rep = None
        WMS = SM.getService("WindowManager")
        self.WMS = WMS.WindowManagerService.instance()

    def request(self, msg):
        _msg = msg.split("|")
        self.req = msg
        if _msg[1] == "UI":
            self.rep = self.WMS.requestUI(msg)




    def reply(self):
        return self.rep