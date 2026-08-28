import os, hashlib, json

class LockSettingsService:
    
    def __init__(self):
        self.__PASSWORD_FILE_PATH__ = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data", "System", "Passwords.json"
        )
        
        self.__VARIFIED_PASSWORD = False
        
    def PasswordAvailable(self):
        with open(self.__PASSWORD_FILE_PATH__, "r") as PF:
            data = json.load(PF)        
            _ = bytes.fromhex(data["salt"])
            if not _:
                return False
            elif  _ == "":
                return False
            else:
                return True
            
    def VarifyPassword(self, password):
        with open(self.__PASSWORD_FILE_PATH__, "r") as PF:
            data = json.load(PF)
        
        SALT = bytes.fromhex(data["salt"])
        if not SALT:
            return "No passwords set"
        password = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            SALT,
            100000
        )

        if password.hex() != data["hash"]:
            return False
        else:
            self.__VARIFIED_PASSWORD = True
            return True
            
            
    def SaveNewPassword(self, password):

        if self.PasswordAvailable() and not self.__VARIFIED_PASSWORD:
            return

        SALT = os.urandom(16)

        KEY = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            SALT,
            100000
        )

        DATA = {
            "salt": SALT.hex(),
            "hash": KEY.hex()
        }
        with open(self.__PASSWORD_FILE_PATH__, "w") as PF:
            json.dump(DATA, PF)
            
            

