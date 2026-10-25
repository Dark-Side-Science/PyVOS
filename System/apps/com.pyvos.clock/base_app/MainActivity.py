import sys
from pyvos.ui.widgets import Button
from pyvos.ui.widgets import Window
from pyvos.ui.widgets import Label
from pyvos.ui.widgets import VerticalLayout

#from pyvos.activity import Activity

class MainActivity:

    def __init__(self):
        super().__init__()
        self.window = Window()
        b = Button("hello")
        b.setText("click me!")
        self.window.resize(360, 640)
        layout = VerticalLayout()
        label = Label("Hello from PyVOS!")
        layout.addWidget(label)
        self.window.setLayout(layout)

    def onCreate(self):
        self.window.show()
