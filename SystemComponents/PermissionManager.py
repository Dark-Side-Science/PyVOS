from system_server.WindowManagerService import HomeScreen
import os, json

class PermissionManager:
    def __init__(self, package):
        self.package = package
        self.screen = HomeScreen
        self.BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        self.__PERMISSION_DIR = os.path.join(self.BASE_DIR, "data", "System", "Permissions")
        
    def write_p(self, app_self, app, permission):
        path = os.path.join(self.__PERMISSION_DIR, f"{self.package}.json")
        data = {}
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
        data.setdefault("granted", [])
                
        if permission not in data["granted"]:
            data["granted"].append(permission)
                
        with open(path, "w") as pf:
            json.dump(data, pf, indent=4)
            
    def read_p(self, app):
        path = os.path.join(self.__PERMISSION_DIR, f"{app}.json")
        if not os.path.exists(path):
            return {
                "granted": [],
                "denied": []
                }
                
        with open(path, 'r') as f:
            return json.load(f)
            
    def remove_p(self, app, permission, mode="granted"):
        path = os.path.join(self.__PERMISSION_DIR, f"{app}.json")
        if not os.path.exists(path):
            return "File not found"
                
        with open(path, 'r') as f:
            data = json.load(f)
        if permission in data.get(mode, []):
            data[mode].remove(permission)
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

        
    def AskPermission(self, permission):
        app = self.app
        if permission == "BackgroundService":
            prompt = f"Allow {type(app).__name__} to start in background?"
        elif permission == "Notification":
            prompt = f"Allow {type(app).__name__} to send you notifications?"
        elif permission == "STORAGE":
            prompt = f"Allow {type(app).__name__} to manage files and storage in the device?"
            
        user = self.screen.AskUserPermission(prompt)
        
        if user == "Allowed":
            pass
        else:
            pass
            