import os, json
from System.bin.mkdir import mkdir
from System.bin.rm import rm
from SystemComponents.PermissionManager import PermissionManager

class FileSystem:

    def __init__(self, storage_mode):
        self.PACKAGE = None
        self.BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        
        self.INTERNAL_FILES_DIR = os.path.join(
            self.BASE_DIR, "storage", "emulated", "0"
        )
        self.APP_DATA_DIR = os.path.join(self.BASE_DIR, "data", "data")
        self.INSTALLED_APPS_DIR = os.path.join(self.BASE_DIR, "data", "app")
        self.storage_loc = self.APP_DATA_DIR if storage_mode == "APP_DATA" else self.INTERNAL_FILES_DIR if storage_mode == "INTERNAL" else self.INTERNAL_FILES_DIR
        if storage_mode == "INTERNAL":
            PM = PermissionManager()
            PM.CheckPermission("STORAGE")

    def __resolve(self, vpath):
        # virtual path → real path
        if vpath.startswith("/"):
            vpath = vpath[1:]
        return os.path.join(self.storage_loc, vpath)
    def return_path(self):
        return self.__resolve('')
        
    def read(self, vpath, binary=False, encoding="utf-8"):
        path = self.__resolve(vpath)
            
        if not os.path.exists(path):
            raise FileNotFoundError(vpath)

        if os.path.isdir(path):
            return "Is a directory"

        try:
            if binary:
                with open(path, "rb") as f:
                    return f.read()
            else:
                with open(path, "r", encoding=encoding) as f:
                    return f.read()
        except PermissionError:
            return "Permission denied"
        except UnicodeDecodeError:
            return "File isn't readable."
        except Exception:
            return "Unknown error occurred."
            
    def write(self, vpath, content, binary=False, encoding="utf-8"):
        path = self.__resolve(vpath)
        try:
            if binary:
                if not isinstance(content, (bytes, bytearray)):
                    return "Binary write expects bytes."
                with open(path, 'wb') as f:
                    f.write(content)
                return
            else:
                if not isinstance(content, str):
                    return "Text write expects str."
                with open(path, "w", encoding=encoding) as f:
                    f.write(content)
                return
        except PermissionError:
            return 'Permission denied.'
        except Exception:
            return "Unknown error occurred."
            
    def remove(self, vpath):
        return rm(vpath)
        
    def makeDir(self, vpath):
        return mkdir(vpath)