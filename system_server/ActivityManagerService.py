import importlib, os
from ..PyVOSRT.app_process import AppProcess

class ActivityManagerService:
    
#    def __init__(self):
         
    def startActivity(self, package, app_path):
        process = AppProcess(app_path, package)
        process.Start()
