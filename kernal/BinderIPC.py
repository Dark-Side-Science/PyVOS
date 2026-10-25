from system_server.WindowManagerService import WindowManagerService
from ..system_server.ServiceManager import ServiceManager as SM

class ID:
    _counter = 0

    @classmethod
    def generate(cls, prefix="OBJ"):
        cls._counter += 1

        return f"{prefix}_{cls._counter:06d}"


class IBinder:
    
    def __init__(self):
        self.req = None
        WMS = SM.getService("WindowManager")
        self.WMS = WMS.WindowManagerService.instance()

    def request(self, msg):
        _msg = msg.split("|")
        self.req = msg
        if _msg[1] == "UI":
            self.WMS.requestUI(msg)




    def reply(self):
        req = self.req.split("|")
        if req[2] == "NEW":
            id = ID.generate(req[3])
            return id
        else:
            return "REQUEST ACCEPTED"