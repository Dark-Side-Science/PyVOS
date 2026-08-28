from pyvos.ui.widgets import Button as B, GridLayout, VerticalBoxLayout, LineEdit, Widget, SizePolicy, HorizontalBoxLayout
from pyvos.graphics import FontMetrics
from pyvos.ui.core import Gravity
from pyvos.graphics import Font, TextCursor, TextBlockFormat



class MainActivity:
    
    def __init__(self, WinManagerClass):
        
        self.win = Widget()
        self.MainWin = WinManagerClass
        self.layout = VerticalBoxLayout()
        self.btnContainer = Widget()
        self.btnFrame = GridLayout()
        self.textView = LineEdit()
        self.textView.setFixedHeight(340)
        self.textView.setText('0')
        self.textView.setReadOnly(True)
        
        self.textView.setAlignment(Gravity.AlignRight | Gravity.AlignBottom)        
        
        self.btnC = B("AC")
        self.btnBack = B("«")
        self.btnPer = B("%")
        self.btnDiv = B("÷")
        self.btn7 = B("7")
        self.btn8 = B("8")
        self.btn9 = B("9")
        self.btnMull = B("×")
        self.btn4 = B("4")
        self.btn5 = B("5")
        self.btn6 = B("6")
        self.btnMin = B("-")
        self.btn1 = B("1")
        self.btn2 = B("2")
        self.btn3 = B("3")
        self.btnAdd = B("+")
        self.btnDot = B(".")
        self.btn0 = B("0")
        self.btnPow = B("^")
        self.btnEqu = B("=")
        
        self.btnFrame.addWidget(self.btnC, 0, 0)
        self.btnFrame.addWidget(self.btnBack, 0, 1)
        self.btnFrame.addWidget(self.btnPer, 0, 2)
        self.btnFrame.addWidget(self.btnDiv, 0, 3)
        self.btnFrame.addWidget(self.btn7, 1, 0)
        self.btnFrame.addWidget(self.btn8, 1, 1)
        self.btnFrame.addWidget(self.btn9, 1, 2)
        self.btnFrame.addWidget(self.btnMull, 1, 3)
        self.btnFrame.addWidget(self.btn4, 2, 0)
        self.btnFrame.addWidget(self.btn5, 2, 1)
        self.btnFrame.addWidget(self.btn6, 2, 2)
        self.btnFrame.addWidget(self.btnMin, 2, 3)
        self.btnFrame.addWidget(self.btn1, 3, 0)
        self.btnFrame.addWidget(self.btn2, 3, 1)
        self.btnFrame.addWidget(self.btn3, 3, 2)
        self.btnFrame.addWidget(self.btnAdd, 3, 3)
        self.btnFrame.addWidget(self.btnDot, 4, 0)
        self.btnFrame.addWidget(self.btn0, 4, 1)
        self.btnFrame.addWidget(self.btnPow, 4, 2)
        self.btnFrame.addWidget(self.btnEqu, 4, 3)
        
        self.btn1.clicked.connect(lambda: self.append_num(1))
        self.btn2.clicked.connect(lambda: self.append_num(2))
        self.btn3.clicked.connect(lambda: self.append_num(3))
        self.btn4.clicked.connect(lambda: self.append_num(4))
        self.btn5.clicked.connect(lambda: self.append_num(5))
        self.btn6.clicked.connect(lambda: self.append_num(6))
        self.btn7.clicked.connect(lambda: self.append_num(7))
        self.btn8.clicked.connect(lambda: self.append_num(8))
        self.btn9.clicked.connect(lambda: self.append_num(9))
        self.btn0.clicked.connect(lambda: self.append_num(0))
        self.btnC.clicked.connect(lambda: self.append_num(0, True))
        self.btnAdd.clicked.connect(lambda: self.append_op("+"))
        self.btnMin.clicked.connect(lambda: self.append_op("-"))
        self.btnMull.clicked.connect(lambda: self.append_op("×"))
        self.btnDiv.clicked.connect(lambda: self.append_op("÷"))
        self.btnEqu.clicked.connect(self.Calculate)
        self.btnDot.clicked.connect(lambda: self.append_op("."))
        self.btnBack.clicked.connect(self.Back)
        self.btnPow.clicked.connect(self.PowMode)
                
        all_buttons = [
    self.btnC, self.btnBack, self.btnPer, self.btnDiv,
    self.btn7, self.btn8, self.btn9, self.btnMull,
    self.btn4, self.btn5, self.btn6, self.btnMin,
    self.btn1, self.btn2, self.btn3, self.btnAdd,
    self.btnDot, self.btn0, self.btnPow, self.btnEqu
]
        for b in all_buttons:
            b.setSizePolicy(SizePolicy.Expanding, SizePolicy.Expanding)
            b.setStyleSheet("""
        Button {
            border-radius: 18px;
            background-color: #FF6F00;
            color: white;
            font-size: 24px;
            padding: 8px;
        }
        Button:hover {
            background-color: #3a3a3a;
        }
        
    """)
    
        self.textView.setStyleSheet("""
    LineEdit {
        color: white;
        background-color: black;
        font-size: 64px
    }
""")
    
        self.btnContainer.setStyleSheet("background-color: #000000;")  # black
        self.win.setStyleSheet("background-color: #000000;")
    
        for i in range(5):
            self.btnFrame.setRowStretch(i, 1)
        for i in range(4):
            self.btnFrame.setColumnStretch(i, 1)
        self.win.setLayout(self.layout)
        self.btnContainer.setLayout(self.btnFrame)
        self.layout.addWidget(self.textView)
        self.layout.addWidget(self.btnContainer)
        bottom_buttons = QHBoxLayout()
        backB = B("◁")
        homeB = B("●")
        recentB = B("■")
        homeB.clicked.connect(self.goHome)
        bottom_buttons.addWidget(backB)
        bottom_buttons.addWidget(homeB)
        bottom_buttons.addWidget(recentB)
        self.layout.addLayout(bottom_buttons)
    
    def goHome(self):
        self.win.hide()
        self.MainWin.show()
        
    def goBack(self):
        self.win.hide()
        self.MainWin.show()
       
    def gotoRecents(self):
        self.win.close()
        self.MainWin.show()
        
    def will_overflow(self, new_text):
        metrics = self.textView.fontMetrics()
        text_width = metrics.horizontalAdvance(new_text)

    # padding + cursor space
        padding = 20
        return text_width + padding > self.textView.width()
    
    def append_op(self, op):
        if self.textView.text().endswith(("+", "-", "×", "÷")) or self.will_overflow(self.textView.text() + op):
            return 
        
        self.textView.setText(self.textView.text() + op)
    


    def append_num(self, num, C=False):
        if C:
            self.textView.setText("0")
            return
        if self.textView.text() == '0':
            self.textView.setText(str(num))
            return
        if self.will_overflow(self.textView.text() + str(num)):
            font = Font()
            font.setPointSize(18)
            return
            self.textView.setFont(font)
        self.textView.setText(self.textView.text() + str(num))
        
        self.textView.setAlignment(Gravity.AlignRight | Gravity.AlignBottom)
        
    def Back(self):
        if len(self.textView.text()) == 1:
            self.textView.setText("0")
            return
        self.textView.setText(self.textView.text()[:-1])
        
    def PowMode(self):
         if self.btnPow.text() == "^":
             self.append_op("^(")
             self.btnPow.setText(")")
         else:
             self.append_op(")")
             self.btnPow.setText("^")
         
    def Show(self):
        self.win.show()

        
    def Calculate(self):
        try:
            ans = str(eval(self.textView.text().replace("×", "*").replace("÷", "/").replace("^", "**")))
        except Exception as e:
            ans = "Error"
        finally:
            self.textView.setText(ans)
            