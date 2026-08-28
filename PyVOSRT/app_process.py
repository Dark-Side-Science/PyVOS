from ..kernal.BinderIPC import IBinder
import subprocess, sys, os, threading
'''
class AppProcess:
    
    def __init__(self, path, package):
        self.path = path
        self.package = package
        self.r1, self.w1 = os.pipe()
        self.r2, self.w2 = os.pipe()
        self.system_binder = IBinder()
        
    def Start(self):
        self.proc = subprocess.Popen(
    ["python", os.path.join(os.path.dirname(__file__), "Runtime.py"), str(self.w1), str(self.r2), self.path, self.package], pass_fds=(self.w1, self.r2), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        os.close(self.w1)
        os.close(self.r2)
        rp = os.fdopen(self.r1)
        wp = os.fdopen(self.w2, "w")
        threading.Thread(target=self.loop, args=(rp, wp), daemon=True).start()
        
    def loop(self, rp, wp):
        while True:
            msg = rp.readline()
            output = self.proc.stdout.readline()
            error = self.proc.stderr.readline()
            if not output.strip() == "" or None:
                print("Child said:", output)
            if not error.strip() == "" or None:
                print("Child throwed:", output)
            if not msg.strip() == "" or None:
                print("Child wrote: ", msg)
                continue
            msg = msg.strip()
            if not msg:
                continue
            
            self.system_binder.request(msg)
            rep = self.system_binder.reply()
            if rep.startswith("REQUEST_ACCEPTED|"):
                pass
            else:
                wp.write(rep + "\n")
                wp.flush()
            print(msg)
'''
import multiprocessing
import threading
import sys
import os


def runtime_entry(runtime_conn, binder_conn, path, package):
    from .Runtime import run_runtime

    run_runtime(
        runtime_conn,
        binder_conn,
        path,
        package
    )


class AppProcess:

    def __init__(self, path, package):

        self.path = path
        self.package = package

        # Runtime communication
        self.runtime_parent, self.runtime_child = (
            multiprocessing.Pipe(duplex=True)
        )

        # Binder communication
        self.binder_parent, self.binder_child = (
            multiprocessing.Pipe(duplex=True)
        )

        self.system_binder = IBinder()

        self.proc = None


    def Start(self):

        self.proc = multiprocessing.Process(
            target=runtime_entry,
            args=(
                self.runtime_child,
                self.binder_child,
                self.path,
                self.package
            ),
            daemon=True
        )

        self.proc.start()

        # Parent doesn't need the child endpoints anymore
        self.runtime_child.close()
        self.binder_child.close()

        threading.Thread(
            target=self.loop,
            daemon=True
        ).start()

    def loop(self):

        while self.proc.is_alive():

            # ==========================================
            # Runtime -> AppProcess
            # ==========================================
            if self.runtime_parent.poll(0.01):

                try:
                    msg = self.runtime_parent.recv()

                except (EOFError, BrokenPipeError, OSError):
                    print("Runtime disconnected.")
                    break

                if not msg:
                    continue

                print("Child wrote:", msg)

                self.system_binder.request(msg)

                rep = self.system_binder.reply()

                if rep and not rep.startswith("REQUEST_ACCEPTED|"):
                    try:
                        self.runtime_parent.send(rep)
                    except (EOFError, BrokenPipeError, OSError):
                        print("Runtime disconnected while sending.")
                        break

            # ==========================================
            # Binder requests from Runtime
            # ==========================================
            if self.binder_parent.poll(0.01):

                try:
                    msg = self.binder_parent.recv()

                except (EOFError, BrokenPipeError, OSError):
                    print("Runtime disconnected.")
                    break

                if not msg:
                    continue

                print("Binder request:", msg)

                self.system_binder.request(msg)

                rep = self.system_binder.reply()

                if rep:
                    try:
                        self.binder_parent.send(rep)
                    except (EOFError, BrokenPipeError, OSError):
                        print("Runtime disconnected while sending.")
                        break

        print("AppProcess IPC loop stopped.")