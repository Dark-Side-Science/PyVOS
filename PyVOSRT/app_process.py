from ..kernal.BinderIPC import IBinder
import subprocess, sys, os, threading
import multiprocessing


def runtime_entry(runtime_conn, binder_conn, path, package):
    import traceback

    print("========== RUNTIME PROCESS START ==========", flush=True)

    try:
        from .Runtime import run_runtime

        print("Runtime called", flush=True)

        run_runtime(
            runtime_conn,
            binder_conn,
            path,
            package
        )

        print("run_runtime returned", flush=True)

    except BaseException as e:
        print("========== RUNTIME CRASH ==========", flush=True)
        print("Exception:", repr(e), flush=True)
        traceback.print_exc()
        print("====================================", flush=True)

        raise

    finally:
        print("========== RUNTIME PROCESS END ==========", flush=True)

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
            daemon=False
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

        while True:

            # If process has died, don't try to communicate with it
            if not self.proc.is_alive():
                print(
                    "Runtime process exited.",
                    "exitcode =", self.proc.exitcode
                )

                break

            # Runtime -> AppProcess
            if self.runtime_parent.poll(0.01):

                try:
                    msg = self.runtime_parent.recv()

                except EOFError:
                    print(
                        "Runtime pipe closed.",
                        "exitcode =",
                        self.proc.exitcode
                    )
                    break

                except (BrokenPipeError, OSError) as e:
                    print("Runtime IPC error:", repr(e))
                    break

                if msg:
                    print("Child wrote:", msg)

                    self.system_binder.request(msg)
                    rep = self.system_binder.reply()

                    if rep and not rep.startswith("REQUEST_ACCEPTED|"):
                        try:
                            self.runtime_parent.send(rep)
                        except (EOFError, BrokenPipeError, OSError) as e:
                            print("Failed sending Runtime reply:", repr(e))
                            break

            # Binder requests from Runtime
            if self.binder_parent.poll(0.01):

                try:
                    req = self.binder_parent.recv()

                except EOFError:
                    print(
                        "Runtime binder pipe closed.",
                        "exitcode =",
                        self.proc.exitcode
                    )
                    break

                except (BrokenPipeError, OSError) as e:
                    print("Binder IPC error:", repr(e))
                    break

                if req:
                    print("Binder request:", req)

                    self.system_binder.request(req)
                    rep = self.system_binder.reply()

                    if rep:
                        try:
                            self.binder_parent.send(rep)
                        except (EOFError, BrokenPipeError, OSError) as e:
                            print("Failed sending binder reply:", repr(e))
                            break

        print("AppProcess IPC loop stopped.")