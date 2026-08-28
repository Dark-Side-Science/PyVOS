class ServiceM:
    _instance = None   # singleton storage

    def __init__(self):
        self.services = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ServiceM()
        return cls._instance

    def RegisterServices(self, services):
        self.services = services

    def getService(self, name):
        return self.services.get(name)
        
ServiceManager = ServiceM.instance()