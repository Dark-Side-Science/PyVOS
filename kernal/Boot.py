import sys, os, platform, subprocess, time, traceback
from datetime import datetime
BOOT_TIME = None
        
class SystemCrash(RuntimeError):
    pass
        

class Boot:
    
    def __init__(self):
        BOOT_TIME = time.time()
        print("Boot loaded at time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().microsecond // 1000)
        log._write("""\n\n\n_–_–_–_–_–_–_–_–_–_–_–_–_–_–_–_–_–
/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\
_–_–_–_–_–_–_–_–_–_–_–_–_–_–_–_–_–\n""", "")
        log.info("Boot loaded time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().microsecond // 1000)
        self._WindowManager = None
        self._PermissionManager = None
        self._Runtime = None
        self._ActivityManager = None
        self._PackageManager = None
        self._TTS = None
        self._Recognizer = None
        self._FileSystem = None
        
    def init(self):
        print("Boot started at time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().microsecond // 1000)
        log.info("Boot started at time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().microsecond // 1000)
        try:
            self.__checkAndInstallMissingSystemRequirements()
            self.__loadSystemServices()
            self.__loadFileSystem()
            self.__loadRuntime()
          # self.__loadSocketSystem()
            self.__loadSpeechService()
            self.__loadWindowService()
        #   self.__loadApps()
          # self.__loadSystemComponents()
            self.__StartOperatingSystem()
            self.__manageLogs()
        except:
            log.error("Initilisation failed")
            raise SystemCrash("Initilisation failed")

    def is_android(self):
        return (
            'ANDROID_ARGUMENT' in os.environ or
            'ANDROID_BOOTLOGO' in os.environ or
            'ANDROID_ROOT' in os.environ or
            'android' in platform.system().lower()
    )
    
    def is_desktop(self):
        if sys.platform.startswith("win") or sys.platform.startswith("linux") or sys.platform == "darwin":
            log.info("Host system recognised as desktop")
            return True
    
    def install(self, pkg):
        result = subprocess.run(
    [sys.executable, "-m", "pip", "install", pkg],
    capture_output=True,
    text=True
    )
        if result.returncode  == 0:
            pass
        else:
            raise ModuleNotFoundError("System Required module not available. Unable to install or import the package. OS abort.")
            
    def __manageLogs(self):

        LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        MAX_DAYS = 7
        now = time.time()
        for file in os.listdir(LOG_DIR):
            path = os.path.join(LOG_DIR, file)
            
            if os.path.isfile(path):
                file_time = os.path.getmtime(path)
                if (now - file_time) > (MAX_DAYS * 86400):
                    os.remove(path)
                    
    
    def __loadSystemServices(self):
        try:
            from ..system_server.ActivityManagerService import ActivityManagerService
            from ..system_server.PackageManagerService import PackageManagerService
            self._ActivityManager = ActivityManagerService()
            self._PackageManager = PackageManagerService()
            log.info("System services loaded successfully")
            print("System services loaded successfully")
        except Exception as e:
            log.error("Failed to import system service(s)\nError: ", e)
            print("Failed to import system service(s)\nError: ", e)

    def __checkAndInstallMissingSystemRequirements(self):
        if self.is_android():
            log.info("Host system recognised as mobile, Android")
            print("Host system recognised as mobile, Android")
            try:
                import PySide6
                log.info("PySide6 linkeable")
                print("PySide6 linkeable")
            except ImportError:
                log.warn("PySide6 unlinkeable, probably not installed\nTrying to install PySide6...")
                print("PySide6 unlinkeable, probably not installed\nTrying to install PySide6...")
                try:                    
                    self.install("pyside6")
                    log.info("PySide6 installed successfully")
                    print("PySide6 installed successfully")
                except:
                    log.error("Failed to install PySide6. System abort.")
                    raise SystemCrash("Failed to load window backend.")
        elif self.is_desktop():
            try:
                import PySide6
                log.info("PySide6 loaded")
                print("PySide6 loaded")
            except ImportError:
                log.warn("PySide6 unlinkable, probably not installed\nTrying to install PySide6...")
                print("PySide6 unlinkable, probably not installed\nTrying to install PySide6...")
                try:                    
                    self.install("pyside6")
                    log.info("PySide6 installed successfully")
                    print("PySide6 installed successfully")
                except Exception as e:
                    log.error("Failed to install PySide6. System abort.\nError: ", e)
                    raise SystemCrash("Failed to load window backend.")
            try:
                from PySide6.QtWebEngineWidgets import QWebEngineView
                log.info("PySide6 loaded")
                print("PySide6 loaded")
            except ImportError:
                log.warn("QtWebEngineView unlinkable, probably not installed\nTrying to install QtWebEngineView...")
                print("QtWebEngineView unlinkable, probably not installed\nTrying to install QtWebEngineView...")
                try:                    
                    self.install("PySide6-WebEngine")
                    log.info("QtWebEngineView installed successfully")
                    print("QtWebEngineView installed successfully")
                except Exception as e:
                    log.error("Failed to install QtWebEngineView. System abort.\nError: ", e)
                    raise SystemCrash("Failed to load web engine.")
                    
    def __loadFileSystem(self):
        try:
            from SystemComponents.FileSystem import FileSystem
            self._FileSystem = FileSystem
            log.info("FileSystem loaded successfully")
            print("FileSystem loaded successfully")
        except Exception as e:
            log.error(f"FileSystem not loadable, probably edited by the user.\nError: {e}")
            raise SystemCrash(f"FileSystem not loadable, probably edited by the user.\nError: {e}")
            
    def __loadRuntime(self):
        try:
            from ..PyVOSRT.Runtime import PyVOSRunTime
            self._Runtime = PyVOSRunTime
            log.info("Runtime laded")
        except IndexError:
            log.info("Runtime loaded")
            print("Runtime loaded")
        except Exception as e:
            log.error("Runtime unloadable, probably edited by the user\nError: ", e)
            raise SystemCrash("Runtime unloadable, probably edited by the user")
    
    def __loadSpeechService(self):
        try:
            from ..system_server.SpeechService.TTS import TextToSpeech
            self._TTS = TextToSpeech
            log.info("Text to speech service loaded")
            print("Text to speech service loaded")
        except Exception as e:
            log.error("Text to speech service unloadable, probably edited by the user\nError: ", e)
            print("Text to speech service unloadable, probably edited by the user\nError: ", e)
            
        try:
            from ..system_server.SpeechService.Recognizer import SpeechRecognizer
            self._Recognizer = SpeechRecognizer
            log.info("Speech recognizer loaded")
            print("Speech recognizer loaded")
        except Exception as e:
            log.error("Speech recognizer unloadable, probably edited by the user\nError: ", e)
            print("Speech recognizer unloadable, probably edited by the user\nError: ", e)
    
    def __loadWindowService(self):
        try:
            from ..system_server import WindowManagerService
            self._WindowManager = WindowManagerService
            log.info("Window manager loaded")
            print("Window manager loaded")
        except Exception as e:
            log.error("Window manager unloadable, probably edited by the user\nError: ", e)
            raise SystemCrash("Window manager unloadable, probably edited by the user")
            
    def __StartOperatingSystem(self):
        print("starting operating system")
        log.info("starting operating system")
        try:
            from ..system_server.SystemServer import SystemServer
            from ..system_server.ServiceManager import ServiceManager
            Services = {
            "ActivityManager" : self._ActivityManager,
            "PackageManager" : self._PackageManager,
            "WindowManager" : self._WindowManager,
            "PermissionManager" : self._PermissionManager,
            "FileSystem" : self._FileSystem}
            self.sm = ServiceManager
            self._SystemServer = SystemServer(Services, self.sm)
            self._SystemServer.start()
        except Exception as e:
           log.error("Starting operating system aborted, an error occured\nError: ", e)
           raise SystemCrash("Starting operating system aborted, an error occured")
           
          

class log:
    
    @staticmethod
    def error(*msg):
        log._write(msg, "ERROR")

    @staticmethod
    def info(*msg):
        log._write(msg, "INFO")

    @staticmethod
    def warn(*msg):
        log._write(msg, "WARN")

    @staticmethod
    def _write(msg, lvl):
        root = os.path.dirname(os.path.dirname(__file__))
        if lvl == "ERROR":
            path = os.path.join(root, "logs", f"{time.strftime('%Y-%m-%d')}_crash.log")	
            base_msg = " ".join(map(str, msg))
            msg = base_msg + "\n" + traceback.format_exc()
        else:
        	path = os.path.join(root, "logs", f"{time.strftime('%Y-%m-%d')}.log")

        timestamp = time.strftime("%H:%M:%S")

        # Join all arguments into one string
        
        if isinstance(msg, str):
            final_msg = msg
        else:        
            final_msg = " ".join(map(str, msg))
        with open(path, "a") as f:
            f.write("""\n
————————————————————————\n""")       
            f.write(f"{timestamp}  [{lvl}]  {final_msg}\n") 