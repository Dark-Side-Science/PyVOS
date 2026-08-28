from PySide6.QtWidgets import QApplication

class SystemTheme:
    def __init__(self):
        print(type(self), "1")
        self.theme = "dark"
        print(type(self), "2")
        self.darkTheme = """QWidget{
        background-color:white;
        color:black;
        }"""
        
    def ToggleTheme(self):
        print(type(self), '3')
        if self.theme == "dark":
            self.SetLite()
        else:
            self.SetDark()
            
    def SetDark(self):
        QApplication.instance().setStyleSheet(self.darkTheme)
        self.theme = "dark"
        
    def SetLite(self):
        QApplication.instance().setStyleSheet("")
        self.theme = "lite"
        