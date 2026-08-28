from PySide6.QtWidgets import QPushButton as Button, QWidget, QGridLayout, QApplication, QSizePolicy, QVBoxLayout
from PySide6.QtWidgets import QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt

        
class PyVOSKeyboard(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
QWidget {
    background-color: #18191A;
}
""")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(260)
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)
        
        self.setLayout(self.layout)
        self.create_buttons()
        self.setup_buttons()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(4)
        self.connect_buttons()
        self.add_buttons()
    def create_buttons(self):
        #First row
        self._1 = Button("1")
        self._2 = Button("2")
        self._3 = Button("3")
        self._4 = Button("4")
        self._5 = Button("5")
        self._6 = Button("6")
        self._7 = Button("7")
        self._8 = Button("8")
        self._9 = Button("9")
        self._0 = Button("0")
        #Second row
        self._q = Button("q")
        self._w = Button("w")
        self._e = Button("e")
        self._r = Button("r")
        self._t = Button("t")
        self._y = Button("y")
        self._u = Button("u")
        self._i = Button("i")
        self._o = Button("o")
        self._p = Button("p")
        #Third row
        self._a = Button("a")
        self._s = Button("s")
        self._d = Button("d")
        self._f = Button("f")
        self._g = Button("g")
        self._h = Button("h")
        self._j = Button("j")
        self._k = Button("k")
        self._l = Button("l")
        #Fourth row
        self._shift = Button()
        self._z = Button("z")
        self._x = Button("x")
        self._c = Button("c")
        self._v = Button("v")
        self._b = Button("b")
        self._n = Button("n")
        self._m = Button("m")
        self._back = Button("⌫")
        #Fifth row
        self._symbol = Button("?123")
        self._comma = Button(",")
        self._space = Button(" ")
        self._dot = Button(".")
        self._newline = Button("⤶")
        
                      
    def setup_buttons(self):
        normal_btns = [self._1, self._2, self._3, self._4, self._5, self._6, self._7, self._8, self._9, self._0, self._q, self._w, self._e, self._r, self._t, self._y, self._u, self._i, self._o, self._p, self._a, self._s, self._d, self._f, self._g, self._h, self._j, self._k, self._l, self._z, self._x, self._c, self._v, self._b, self._n, self._m]
                   
        for btn in normal_btns:
            btn.setMinimumSize(30, 45)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("""
    QPushButton {
        background-color: #2B2B2B;
        color: white;
        border-radius: 10px;  /* half of width/height = perfect circle */
        border: none;
        font-size: 14px;
    }
    QPushButton:pressed {
    background-color: #5F6368;
}
            """)
            
        self._shift.setFixedSize(50, 40)
        self._shift.setStyleSheet("""
    QPushButton {
        background-color: #2C4654;
        color: white;
        border-radius: 10px;  /* half of width/height = perfect circle */
        border: none;
        font-size: 14px;
    }
        QPushButton:pressed {
    background-color: #5F6368;
}
            """)
            
        self._back.setFixedSize(50, 40)
        self._back.setStyleSheet("""
    QPushButton {
        background-color: #2C4654;
        color: white;
        border-radius: 10px;  /* half of width/height = perfect circle */
        border: none;
        font-size: 14px;
    }
        QPushButton:pressed {
    background-color: #5F6368;
}
            """)
        
        self._symbol.setFixedSize(50, 48)
        self._symbol.setStyleSheet("""
    QPushButton {
        background-color: #2C4654;
        color: white;
        border-radius: 22px;  /* half of width/height = perfect circle */
        border: none;
        font-size: 14px;
    }
    QPushButton:pressed {
    background-color: #5F6368;
}
""")
            
        self._newline.setFixedSize(50, 48)
        self._newline.setStyleSheet("""
    QPushButton {
        background-color: #2C4654;
        color: white;
        border-radius: 22px;  /* half of width/height = perfect circle */
        border: none;
        font-size: 14px;
    }
    QPushButton:pressed {
    background-color: #5F6368;
}
""")

        self._comma.setFixedSize(34, 47)
        self._comma.setStyleSheet("""
    QPushButton {
        background-color: #2C4654;
        color: white;
        border-radius: 10px;  /* half of width/height = perfect circle */
        border: none;
        font-size: 14px;
    }
    QPushButton:pressed {
    background-color: #5F6368;
}""")

        self._space.setFixedHeight(40)

        self._dot.setFixedSize(34, 47)
        self._dot.setStyleSheet("""
    QPushButton {
        background-color: #2C4654;
        color: white;
        border-radius: 10px;  /* half of width/height = perfect circle */
        border: none;
        font-size: 14px;
    }
    QPushButton:pressed {
    background-color: #5F6368;
}""")

 #       btn.setIcon(QIcon(icon_))
#        btn.setIconSize(QSize(64, 64))

    def connect_buttons(self):
        btns = {
        "1": self._1,
         "2": self._2,
         "3": self._3, 
         "4": self._4, 
         "5": self._5, 
         "6": self._6, 
         "7": self._7, 
         "8": self._8, 
         "9": self._9, 
         "0": self._0, 
         "q": self._q, 
         "w": self._w, 
         "e": self._e, 
         "r": self._r, 
         "t": self._t, 
         "y": self._y, 
         "u": self._u, 
         "i": self._i, 
         "o": self._o, 
         "p": self._p, 
         "a": self._a, 
         "s": self._s, 
         "d": self._d, 
         "f": self._f, 
         "g": self._g, 
         "h": self._h, 
         "j": self._j, 
         "k": self._k, 
         "l": self._l, 
         "z": self._z, 
         "x": self._x, 
         "c": self._c, 
         "v": self._v, 
         "b": self._b, 
         "n": self._n, 
         "m": self._m,
         " ": self._space,
         "back": self._back,
         "\n": self._newline,
         "^": self._shift,
         "sym": self._symbol}
        
        for val, btn in btns.items():
            btn.clicked.connect(lambda checked=False, val=val: self.KeyPressed(val))
            
            
    def KeyPressed(self, val):
        if val == " ":
            pass #self.__IMM.handle_spacekey()
        elif val == "^":
            pass #self.ShiftKeys()
        elif val == "back":
            pass #self.__IMM.handle_backspace()
        elif val == "sym":
            pass #self.Symbols()
        elif val == "\n":
            pass #self.__IMM.handle_enterkey()
        else:
            pass #self.__IMM.handle_key(val)
                
    def add_buttons(self):
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setRowStretch(0, 0)
        #First row
        self.layout.setColumnStretch(0, 0)
        self.layout.addWidget(self._1, 0, 0)
        self.layout.addWidget(self._2, 0, 1)
        self.layout.addWidget(self._3, 0, 2)
        self.layout.addWidget(self._4, 0, 3)
        self.layout.addWidget(self._5, 0, 4)
        self.layout.addWidget(self._6, 0, 5)
        self.layout.addWidget(self._7, 0, 6)
        self.layout.addWidget(self._8, 0, 7)
        self.layout.addWidget(self._9, 0, 8)
        self.layout.addWidget(self._0, 0, 9)
        #Second row
        self.layout.addWidget(self._q, 1, 0)
        self.layout.addWidget(self._w, 1, 1)
        self.layout.addWidget(self._e, 1, 2)
        self.layout.addWidget(self._r, 1, 3)
        self.layout.addWidget(self._t, 1, 4)
        self.layout.addWidget(self._y, 1, 5)
        self.layout.addWidget(self._u, 1, 6)
        self.layout.addWidget(self._i, 1, 7)
        self.layout.addWidget(self._o, 1, 8)
        self.layout.addWidget(self._p, 1, 9)
        #Thrid row
        self.layout.addItem(QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 2, 0)
        self.layout.addWidget(self._a, 2, 1)
        self.layout.addWidget(self._s, 2, 2)
        self.layout.addWidget(self._d, 2, 3)
        self.layout.addWidget(self._f, 2, 4)
        self.layout.addWidget(self._g, 2, 5)
        self.layout.addWidget(self._h, 2, 6)
        self.layout.addWidget(self._j, 2, 7)
        self.layout.addWidget(self._k, 2, 8)
        self.layout.addWidget(self._l, 2, 9)
        self.layout.addItem(QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 2, 10)
        #Fourth row
        self.layout.addWidget(self._shift, 3, 0)
        self.layout.addWidget(self._z, 3, 2)
        self.layout.addWidget(self._x, 3, 3)
        self.layout.addWidget(self._c, 3, 4)
        self.layout.addWidget(self._v, 3, 5)
        self.layout.addWidget(self._b, 3, 6)
        self.layout.addWidget(self._n, 3, 7)
        self.layout.addWidget(self._m, 3, 8)
        self.layout.addWidget(self._back, 3, 9)
        #Fifth row
        self.layout.addWidget(self._symbol, 4, 0)
        self.layout.addWidget(self._comma, 4, 2)
        self.layout.addWidget(self._space, 4, 3, 1, 5)
        self.layout.addWidget(self._dot, 4, 7)
        self.layout.addWidget(self._newline, 4, 9)
        for i in range(10):
            self.layout.setColumnStretch(i, 1)
    


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.setStyleSheet("background-color: #18191A;")
        self.keyboard = PyVOSKeyboard()
        self.keyboard.setParent(self)

        #self.keyboard.setFixedHeight(250)

    def resizeEvent(self, event):
        self.keyboard.setGeometry(
            0,
            self.height() - self.keyboard.height(),
            self.width(),
            self.keyboard.height()
        )
        
if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()