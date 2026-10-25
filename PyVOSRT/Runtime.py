import os, importlib, datetime, sys, subprocess, builtins, threading
import time
from PySide6.QtWidgets import QApplication

from .BinderProxy import BinderProxy

BASE = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class SafeImporter:
    """
    Safe import handler to restrict dangerous libraries in apps.
    """
    def __init__(self, whitelist=None, blacklist=None):
        """
        whitelist: list of allowed module names (if set, only these can be imported)
        blacklist: list of disallowed module names
        """
        self.whitelist = set(whitelist) if whitelist else None
        self.blacklist = set(blacklist) if blacklist else set([ #os, sys, subprocess, builtins, "shutil", "ctypes", "socket", "threading", "multiprocessing"
           "abc123455"
        ])
        # Store original __import__ function
        self._original_import = builtins.__import__
        self.enable()

    def enable(self):
        """Replace built-in __import__ with safe version"""
        builtins.__import__ = self._safe_import

    def disable(self):
        """Restore original __import__"""
        builtins.__import__ = self._original_import

    def _safe_import(self, name, globals=None, locals=None, fromlist=(), level=0):
        # Check blacklist first
        if name.split('.')[0] in self.blacklist:
            raise ImportError(f"No module named '{name}'.")

        # If whitelist exists, only allow those
        if self.whitelist and name.split('.')[0] not in self.whitelist:
            raise ImportError(f"No module named '{name}'")

        # Otherwise, perform normal import
        return self._original_import(name, globals, locals, fromlist, level)

    def is_safe(self, name):
        """Check if a module is safe to import"""
        if name.split('.')[0] in self.blacklist:
            return False
        if self.whitelist and name.split('.')[0] not in self.whitelist:
            return False
        return True
        
        
        
        
class PyVOSRunTime:
    isRunning = False
    
    def __init__(self, path, package):
        print("Runtime called", flush=True)
        self.app_path = path
        Log.PACKAGE = package
        Log.LOG_OPEN = open
        self.isRunning = True
        self._RuntimeBuiltins = {}
        for name in dir(builtins):
            self._RuntimeBuiltins[name] = getattr(builtins, name)
       # self._RuntimeBuiltins.pop("print", None)
        self._RuntimeBuiltins.pop("builtins", None)
        self._RuntimeBuiltins.pop("open", None)
        self._RuntimeBuiltins.pop("eval", None)
        self._RuntimeBuiltins.pop("exec", None)
        self._RuntimeBuiltins.pop("compile", None)
        self._RuntimeBuiltins["Log"] = Log
        
        self.app_dir = os.path.join(self.app_path, "base_app")
        self.PyVOS_import_path = os.path.join(BASE, "PyVOS", "Frameworks", "API")
        sys.path.insert(0, self.PyVOS_import_path)
        sys.path.insert(0, self.app_dir)
        print("Runtime setup done", flush=True)

    def start_lifecycle(self):
        print("lifecycle started", flush=True)

        path = os.path.join(
            self.app_path,
            "base_app",
            "MainActivity.py"
        )

        print("Loading:", path, flush=True)

        spec = importlib.util.spec_from_file_location(
            "MainActivity",
            path
        )

        print("after specs", flush=True)

        module = importlib.util.module_from_spec(spec)

        module.__dict__["__builtins__"] = self._RuntimeBuiltins

        print("importing MainActivity...", flush=True)

        spec.loader.exec_module(module)

        print("MainActivity.py loaded", flush=True)

        MainActivity = getattr(module, "MainActivity")

        print("MainActivity class found", flush=True)

        print("Creating MainActivity...", flush=True)
        self.activity = MainActivity()
        print("MainActivity created", flush=True)
        print("Showing MainActivity...", flush=True)
        self.activity.onCreate()
        print("MainActivity shown", flush=True)
        
    def pause_lifecycle(self):
        self.app.onPause()
        
    def resume_lifecycle(self):
        self.app.onResume()
        
    def stop_lifecycle(self):
        self.app.onDestroy()
        
        
class Log:
    PACKAGE = None
    LOG_OPEN = None
    @staticmethod
    def D(*args):
        Log._write("DEBUG", *args)

    @staticmethod
    def I(*args):
        Log._write("INFO", *args)

    @staticmethod
    def W(*args):
        Log._write("WARN", *args)

    @staticmethod
    def E(*args):
        Log._write("ERROR", *args)
        
    @staticmethod
    def _write(level, *args):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "data", Log.PACKAGE, 'logs', f"{datetime.datetime.now().strftime('%Y-%m-%d')}.txt")
        m = "w" if not os.path.exists(path) else "a"
        msg = " ".join(map(str, args))
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp}  [{level}]  {msg}\n"

        with Log.LOG_OPEN(path, m) as f:
            f.write(line)        

def runtime_loop(runtime, runtime_conn, binder_conn):

    binder = BinderProxy(binder_conn, runtime.package)

    # Make Binder available to framework UI classes
    setBinderForWidgets(binder)
    runtime.start_lifecycle()

    # Tell AppProcess that Runtime started
    runtime_conn.send("hello")

    while runtime.isRunning:

        if runtime_conn.poll(0.1):

            msg = runtime_conn.recv()

            if not msg:
                continue

            msg = msg.strip()

            if msg == "LIFECYCLE|PAUSECYCLE":
                runtime.pause_lifecycle()

            elif msg == "LIFECYCLE|RESUMELIFECYCLE":
                runtime.resume_lifecycle()

            elif msg == "LIFECYCLE|STOPLIFECYCLE":
                runtime.stop_lifecycle()
                break

            else:
                binder.send_request(msg)


import threading
import time

def run_runtime(runtime_conn, binder_conn, path, package):

    print("========== RUN_RUNTIME ==========", flush=True)

    print(
        "runtime_conn closed:",
        runtime_conn.closed,
        flush=True
    )

    print(
        "binder_conn closed:",
        binder_conn.closed,
        flush=True
    )

    runtime = PyVOSRunTime(path, package)

    print("Runtime setup done", flush=True)
    from pyvos.ui.widgets import setBinderForWidgets
    binder = BinderProxy(binder_conn, package)

    print("BinderProxy created", flush=True)

    setBinderForWidgets(binder)

    print("Starting lifecycle...", flush=True)

    runtime.start_lifecycle()

    print("Lifecycle returned!", flush=True)

    while True:
        time.sleep(1)


