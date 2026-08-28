import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
def mkdir(vpath, parents=False):
    if vpath.startswith("/"):
            vpath = vpath[1:]
    path = os.path.join(BASE_DIR, vpath)

    try:
        if parents:
            os.makedirs(path, exist_ok=False)
        else:
            os.mkdir(path)
        return 
        
    except FileExistsError:
        return "File or directory already exists"
    except FileNotFoundError:
        return "Parent directory does not exist"
    except PermissionError:
        return PermissionError("Permission denied")
    except Exception:
        return "Unknown error occurred"
        