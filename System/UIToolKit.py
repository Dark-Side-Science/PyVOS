from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QTextEdit, QLabel
from PySide6.QtGui import QPainter, QPaintEvent, QColor, QMouseEvent
from PySide6.QtCore import QTimer, Signal, QEvent, Qt, QPoint
import sys


class Button(QPushButton):
    LongPressed = Signal()
    
    def __init__(self, text="", parent=None, long_press_ms=1000):
        super().__init__(text, parent)
        self._longpress_ms = long_press_ms
        self._enabled = True
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._long_pressed = False
        self._timer.timeout.connect(self._onLongPressed)
        

    # -------------------------
    # State overrides
    # -------------------------
    def setLongPressDelay(self, ms):
        self._longpress_ms = ms
        
    def _onLongPressed(self):
        self._long_pressed = True
        self.LongPressed.emit()
        
    def setEnabled(self, enabled: bool):
        self._enabled = enabled
        super().setEnabled(enabled)
        self.update()

    def isEnabled(self):
        return self._enabled

    # -------------------------
    # Event overrides
    # -------------------------
    def mousePressEvent(self, event):
        if not self._enabled:
            event.ignore()
            return
        self._long_pressed = False
        self._timer.start(self._longpress_ms)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._timer.stop()
        if not self._long_pressed:
            super().mouseReleaseEvent(event)
        else:
            event.accept()

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        
            
    # -------------------------
    # Paint override (optional)
    # -------------------------
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        if not self._enabled:
            painter.setOpacity(0.4)

        super().paintEvent(event)
        
        

class Window(QWidget):
    tapped = Signal(QPoint)
    longPressed = Signal(QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.setMouseTracking(True)

        self._press_pos = None
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(600)
        self._timer.timeout.connect(self._emit_long)

    # ---------------- Touch ----------------


    def event(self, event):
        etype = event.type()

        if etype == QEvent.Type.TouchBegin:
            pos = event.points()[0].position().toPoint()
            self._start_press(pos)
            return True

        if etype == QEvent.Type.TouchEnd:
            self._end_press()
            return True

        return super().event(event)
    # ---------------- Mouse fallback ----------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._start(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._end()

    # ---------------- Logic ----------------
    def setLongPressDelay(self, ms):
        self._timer.setInterval(ms)
        
    def _start_press(self, pos):
        self._press_pos = pos
        self._timer.start()

    def _end_press(self):
        if self._timer.isActive():
            self._timer.stop()
            self.tapped.emit(self._press_pos)
        self._press_pos = None

    def _emit_long(self):
        if self._press_pos:
            self.longPressed.emit(self._press_pos)
            


class TextView(QLabel):
    clicked = Signal(QPoint)
    pressed = Signal(QPoint)
    released = Signal(QPoint)

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.setMouseTracking(True)

        self._pressed = False
        self._press_pos = QPoint()

    # ========================
    # Core event dispatcher
    # ========================
    def event(self, event):
        etype = event.type()

        if etype == QEvent.Type.TouchBegin:
            pos = event.points()[0].position().toPoint()
            self._on_press(pos)
            return True

        elif etype == QEvent.Type.TouchEnd:
            self._on_release()
            return True

        return super().event(event)

    # ========================
    # Mouse events (fallback)
    # ========================
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._on_press(event.position().toPoint())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._pressed:
            self._on_release()
        super().mouseReleaseEvent(event)

    # ========================
    # Hover events
    # ========================
    def enterEvent(self, event):
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update()
        super().leaveEvent(event)

    # ========================
    # Painting
    # ========================
    def paintEvent(self, event):
        p = QPainter(self)

        # background
        if self._pressed:
            p.fillRect(self.rect(), QColor("#444"))
        else:
            p.fillRect(self.rect(), QColor("#222"))

        # text
        p.setPen(Qt.white)
        p.drawText(self.rect(), Qt.AlignCenter, self.text())

    # ========================
    # Geometry
    # ========================
    def resizeEvent(self, event):
        super().resizeEvent(event)

    def sizeHint(self):
        return super().sizeHint()

    def minimumSizeHint(self):
        return super().minimumSizeHint()

    # ========================
    # State / content
    # ========================
    def setText(self, text):
        super().setText(text)
        self.update()

    def changeEvent(self, event):
        if event.type() == QEvent.Type.EnabledChange:
            self.update()
        super().changeEvent(event)

    # ========================
    # Internal logic
    # ========================
    def _on_press(self, pos: QPoint):
        self._pressed = True
        self._press_pos = pos
        self.pressed.emit(pos)
        self.update()

    def _on_release(self):
        self._pressed = False
        self.released.emit(self._press_pos)
        self.clicked.emit(self._press_pos)
        self.update()
        

class EditText(QTextEdit):
    tapped = Signal(QPoint)        # Emits tap position
    longPressed = Signal(QPoint)   # Emits long press position

    def __init__(self, parent=None):
        super().__init__(parent)

        # Enable touch events
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Long press timer
        self._press_pos = None
        self._long_timer = QTimer(self)
        self._long_timer.setInterval(600)  # ms for long press
        self._long_timer.timeout.connect(self._emit_long_press)

    # ================= TOUCH EVENTS =================
    def event(self, e):
        if e.type() == e.Type.TouchBegin:
            touch = e.points()[0]
            self._press_pos = touch.position().toPoint()
            self._long_timer.start()
            return True

        elif e.type() == e.Type.TouchEnd:
            if self._long_timer.isActive():
                self._long_timer.stop()
                self.tapped.emit(self._press_pos)
            return True

        elif e.type() == e.Type.TouchCancel:
            self._long_timer.stop()
            return True

        return super().event(e)

    # ================= LONG PRESS =================
    def _emit_long_press(self):
        self._long_timer.stop()
        if self._press_pos:
            self.longPressed.emit(self._press_pos)

