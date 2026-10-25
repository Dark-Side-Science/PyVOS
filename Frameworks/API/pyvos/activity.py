import uuid


class Activity:

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.package = None
        self.name = None
        self.state = "CREATED"
        self.window = None

    def onCreate(self):
        pass
     #   self.window.show()
       # self.onStart()
    def onStart(self):
        pass

    def onResume(self):
        pass

    def onPause(self):
        pass

    def onStop(self):
        pass

    def onDestroy(self):
        pass