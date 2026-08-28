WIDGET_REGISTRY = {}
LAYOUT_REGISTRY = {}
_binder = None

def get_widget_by_id(wid):
    return WIDGET_REGISTRY.get(wid)

def get_layout_by_id(lid):
    return LAYOUT_REGISTRY.get(lid)

def setBinderForWidgets(binder):
    global _binder
    _binder = binder

class Button:
    
    def __init__(self, text=""):
        self._text = text
        if not _binder:
            raise RuntimeError("Binder proxy not initialised.")
        if not self.text:
            _binder.send_request("NEW|PUSHBUTTON|NO_TEXT")
            self.WIDGET_ID = _binder.get_response()
            WIDGET_REGISTRY[self.WIDGET_ID] = self
        else:
            if isinstance(text, str):
                _binder.send_request(f"NEW|PUSHBUTTON|TEXT|[{text}]")
                self.WIDGET_ID = _binder.get_response()
            else:
                raise TypeError("pyvos ui component (Button) called with wrong argment type. Supported argument type: str")
        
    def setText(self, text):
        if not isinstance(text, str):
            raise TypeError("pyvos ui component method (Button.setText) called with wrong argument type. Supported argument type: str")
        else:
            _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|SET_TEXT|{text}")
            self._text = text
            
    def setIcon(self, icon_p):
        _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|SET_ICON|{icon_p}")
        response = _binder.get_response(blocking=False)
        if response.split("|")[0] == "BUTTON_ID" and response.split("|")[1] == self.WIDGET_ID and response.split("|")[2] == "ERROR":
            raise FileNotFoundError(f"No such image file '{icon_p}' found.")
    
    def setIconSize(self, w, h):
        if not (isinstance(w, int) and isinstance(h, int)):
            raise TypeError("pyvos ui component method (Button.setIconSize) called with wrong argument type. Supported argument type: int")
        _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|SET_ICON_SIZE|{w}|{h}")
        
    def setCheckable(self, val):
        if not isinstance(val, bool):
            raise TypeError("pyvos ui component method (Button.setCheckable) called with wrong argument type. Supported argument type: bool")
        _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|SET_CHECKABLE|{val}")
        
    def setEnabled(self, val):
        if not isinstance(val, bool):
            raise TypeError("pyvos ui component method (Button.setEnabled) called with wrong argument type. Supported argument type: bool")
        _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|SET_ENABLED|{val}")
        
    def setDisabled(self, val):
        if not isinstance(val, bool):
            raise TypeError("pyvos ui component method (Button.setDisabled) called with wrong argument type. Supported argument type: bool")
        _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|SET_DISABLED|{val}")
        
    def setToolTip(self, text):
        if not isinstance(text, str):
            raise TypeError("pyvos ui component method (Button.setToolTip) called with wrong argument type. Supported argument type: str")
        _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|SET_TOOLTIP|{text}")
        
    def text(self):
        return self._text
                
    def isCheckable(self):
        _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|CHECKABLE")
        msg = _binder.get_response()
        if msg.startswith(f"BUTTON_ID|{self.WIDGET_ID}"):
            parts = msg.split("|")
            if parts[2] == "CHECKABLE":
                return parts[3].lower() == "true"
                
    def isChecked(self):
        _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|CHECKED")
        msg = _binder.get_response()
        if msg.startswith(f"BUTTON_ID|{self.WIDGET_ID}"):
            parts = msg.split("|")
            if parts[2] == "CHECKED":
                return parts[3].lower() == "true"
                
    def isEnabled(self):
        _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|ENABLED")
        msg = _binder.get_response()
        if msg.startswith(f"BUTTON_ID|{self.WIDGET_ID}"):
            parts = msg.split("|")
            if parts[2] == "ENABLED":
                return parts[3].lower() == "true"
                
    def toolTip(self):
        _binder.send_request(f"BUTTON_ID|{self.WIDGET_ID}|TOOLTIP")
        msg = _binder.get_response()
        if msg.startswith(f"BUTTON_ID|{self.WIDGET_ID}"):
            parts = msg.split("|")
            if parts[2] == "TOOLTIP":
                return parts[3]
                
    
    def getWidgetID(self):
        return self.WIDGET_ID
                
                
                
                
                
class GridLayout:        
    def __init__(self):
        _binder.send_request("NEW|GRIDLAY")
        self.WIDGET_ID = binder.get_response()
        LAYOUT_REGISTRY[self.WIDGET_ID] = self
        
    def addWidget(self, widget, row, column, rowSpan=1, columnSpan=1, alignment=0):
        if not (isinstance(columnSpan, int) and isinstance(row, int) and isinstance(column, int) and isinstance(rawSpan, int) and isinstance(alignment, int)):
            raise TypeError("pyvos ui component method (GridLayout.addWidget) called with wrong argument type. Supported types: widget, int, int, int, int, int.")
        widget_id = widget.getWidgetID()    
        req = f"GRIDLAY_ID|{self.WIDGET_ID}|ADDWID|{widget_id}|{row}|{column}|{rowSpan}|{columnSpan}|{alignment}"
        _binder.send_request(req)
        
    def addLayout(self, layout, row, column, rowSpan=1, columnSpan=1):
        if not (isinstance(columnSpan, int) and isinstance(row, int) and isinstance(column, int) and isinstance(rawSpan, int)):
            raise TypeError("pyvos ui component method (GridLayout.addLayout) called with wrong argument type. Supported types: layout, int, int, int, int.")
        id = layout.getWidgetID()
        _binder.send_request(f"GRIDLAY_ID|{self.WIDGET_ID}|ADDLAY|{id}|{row}|{column}|{rowSpan}|{columnSpan}")
        
    def setSpacing(self, spacing):
        if not isinstance(spacing, int):
            raise TypeError("pyvos ui component method (GridLayout.setSpacing) called with wrong argument type. Supported type: int.")
        _binder.send_request(f"GRIDLAY_ID|{self.WIDGET_ID}|SPACING|{spacing}")
    
    def setHorizontalSpacing(self, spacing):
        if not isinstance(spacing, int):
            raise TypeError("pyvos ui component method (GridLayout.setPsacing) called with wrong argument type. Supported type: int.")
        _binder.send_request("GRIDLAY_ID|{self.WIDGET_ID}|H_SPACING|{spacing}")
    
    def setVerticalSpacing(self, spacing):
        if not isinstance(spacing, int):
            raise TypeError("pyvos ui component method (GridLayout.setSpacing) called with wrong argument type. Supported type: int.")
        _binder.send_request("GRIDLAY_ID|{self.WIDGET_ID}|V_SPACING|{spacing}")
        
    def setContentsMargins(self, left, top, right, bottom):
        if not (isinstance(bottom, int) and isinstance(left, int) and isinstance(top, int) and isinstance(right, int)):
            raise TypeError("pyvos ui component method (GridLayout.setContentsMargins) called with wrong argument type. Supported type: int.")
        _binder.send_request(f"GRIDLAY_ID|{self.WIDGET_ID}|CONTENTS_MARGINS|{left}|{top}|{bottom}|{right}")
    
    def setRowStretch(self, row, stretch):
        if not (isinstance(stretch, int) and isinstance(row, int)):
            raise TypeError("pyvos ui component method (GridLayout.setRowStretch) called with wrong argument type. Supported type: int")
        _binder.send_request(f"GRIDLAY_ID|{self.WIDGET_ID}|RSTRETCH|{row}|{stretch}")
        
    def setColumnStretch(self, column, stretch):
        if not (isinstance(stretch, int) and isinstance(column, int)):
            raise TypeError("pyvos ui component method (GridLayout.setRowStretch) called with wrong argument type. Supported type: int")
        _binder.send_request(f"GRIDLAY_ID|{self.WIDGET_ID}|CSTRETCH|{column}|{stretch}")
    
    def setRowMinimumHeight(self, row, minSize):
        if not (isinstance(minSize, int) and isinstance(row, int)):
            raise TypeError("pyvos ui component method (GridLayout.setRowMinimumHeight) called with wrong argument type. Supported type: int")
        _binder.send_request(f"GRIDLAY_ID|{self.WIDGET_ID}|ROWMH|{row}|{minSize}")
        
    def setColumnMinimumWidth(self, column, minSize):
        if not (isinstance(minSize, int) and isinstance(column, int)):
            raise TypeError("pyvos ui component method (GridLayout.setColumnMinimumWidth) called with wrong argument type. Supported type: int")
        _binder.send_request(f"GRIDLAY_ID|{self.WIDGET_ID}|COLMH|{column}|{minSize}")
    
    def itemAtPosition(self, row, column):
        if not (isinstance(row, int) and isinstance(column, int)):
            raise TypeError("pyvos ui component method (GridLayout.itemAtPosition) called with wrong argument type. Supported type: int.")
        _binder.send_request(f"GRIDLAY_ID|{self.WIDGET_ID}|ITEM_AT|{row}|{column}")
        res = _binder.get_response()
        if res.startswith(f"GRID_ID|{self.WIDGET_ID}"):
            parts = res.split("|")
            if parts[2] == "ITEM_AT":
                if parts[3] == "LAY":
                    id = parts[4] 
                    return get_layout_by_id(id)
                elif parts[3] == "WID":
                    id = parts[4] 
                    return get_widget_by_id(id)

    def rowCount(self):
        _binder.send_request(f"GRID_ID|{self.WIDGET_ID}|ROW_COUNT")
        res = _binder.get_response()
        if res.startswith(f"GRID_ID|{self.WIDGET_ID}"):
            parts = res.split("|")
            if parts[3] == "ROW_COUNT":
                return parts[4]
                
    def columnCount(self):
        _binder.send_request(f"GRID_ID|{self.WIDGET_ID}|COL_COUNT")
        res = _binder.get_response()
        if res.startswith(f"GRID_ID|{self.WIDGET_ID}"):
            parts = res.split("|")
            if parts[3] == "COL_COUNT":
                return parts[4]
                
    def setAlignment(self, widget, alignment):
        if not isinstance(alignment, str):
            raise TypeError("pyvos ui component method (GridLayout.setAlignment) called with wrong argument type. Supported type: int.")
        id = widget.getWidgetID()
        _binder.send_request(f"GRID_ID|{self.WIDGET_ID}|SET_ALIGNMENT|{id}|{alignment}")
        
#GridLayout, VerticalBoxLayout, LineEdit, Widget, SizePolicy, HorizontalBoxLayout        
#BUTTON_ID|{self.WIDGET_ID}|SET_TEXT|{text}