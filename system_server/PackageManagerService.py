import os
import xml.etree.ElementTree as ET


class PackageManagerService:
    
    def __init__(self):
        self.__SYSTEM_APPS_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "System", "apps")
        self.__USER_INSTALLED_APPS_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "app")
        
        self.app_names = []
        for i in os.listdir(self.__SYSTEM_APPS_DIRECTORY):
            if i not in ("__init__.py", "__pycache__", "SystemLinker.py"):
                self.app_names.append(i)
        for i in os.listdir(self.__USER_INSTALLED_APPS_DIRECTORY):
            self.app_names.append(i)
        self.__loaded_packages = []
        self.__loaded_manifests = []
        self.__loadPackages()
        
    def __loadPackages(self):
        system_packages = os.listdir(self.__SYSTEM_APPS_DIRECTORY) 
        for package in system_packages:
            if not package.startswith("com") and not package.startswith("org"):
                continue
            self.__loaded_packages.append(package)
            self.__loaded_manifests.append(os.path.join(self.__SYSTEM_APPS_DIRECTORY, package, "base_app", "PyVOSManifest.xml"))
            

        user_packages = os.listdir(self.__USER_INSTALLED_APPS_DIRECTORY)
        for package in user_packages:
            if not package.startswith("com") and not package.startswith("org"):
                continue
            self.__loaded_packages.append(package)
            self.__loaded_manifests.append(os.path.join(self.__USER_INSTALLED_APPS_DIRECTORY, package, "base_app", "PyVOSManifest.xml"))

    def getApplicationIcon(self, pkgname):
        if pkgname in os.listdir(self.__USER_INSTALLED_APPS_DIRECTORY):
            print("user")
        elif pkgname in os.listdir(self.__SYSTEM_APPS_DIRECTORY):
            print("system")
        else:
            print("not user or system")
        return f"/storage/emulated/0/PyVOS/System/apps/{pkgname}/res/ic_launcher/Settings_icon.jpg"
            
    def getInstalledPackages(self):
        return self.__loaded_packages
        
    def NumOfApps(self):        
        return len(self.app_names)
    
        
    def getPackageInfo(self, package):

        path = os.path.join(self.__SYSTEM_APPS_DIRECTORY, package)
        if package in os.listdir(self.__SYSTEM_APPS_DIRECTORY):
            tree = ET.parse(os.path.join(os.path.dirname(os.path.dirname(__file__)), "System", "apps", package, "base_app", "PyVOSManifest.xml"))
        elif package in os.listdir(self.__USER_INSTALLED_APPS_DIRECTORY):
            tree = ET.parse(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "app", package, "base_app", "PyVOSManifest.xml"))
        root = tree.getroot()
        _icon_path = root.attrib["icon"]
        if package in os.listdir(self.__SYSTEM_APPS_DIRECTORY):
            icon_path = _icon_path.replace("@", f"/System/apps/{package}/res/")
        else:
            icon_path = _icon_path.replace("@", f"/data/app/{package}/res/")
        return PackageInfo(root.attrib["package"], path, root.attrib["version"], root.attrib["name"], permissions = [perm.attrib["name"] for perm in root.findall(".//permissions/permission")], icon_path = icon_path)
        
#    def InstallPackage(self, package):
        

class PackageInfo:
    
    def __init__(self, package, path, version, name, permissions, icon_path):
        self.packageName = package
        self.sourceDir = path
        self.requestedPermissions = permissions
        self.label = name
        self.icon_path = icon_path
        self.versionInfo = version
        
        
