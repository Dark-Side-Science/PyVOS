from collections import deque

class Stdin:
    def __init__(self):
        self.buffer = deque()

    def write(self, data):
        """Runtime or pipe writes data to stdin"""
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        self.buffer.append(data)

    def read(self):
        """Program reads all available input"""
        if not self.buffer:
            return ""
        data = "".join(self.buffer)
        self.buffer.clear()
        return data

    def readline(self):
        """Read one line"""
        if not self.buffer:
            return ""
        return self.buffer.popleft()

    def available(self):
        """Check if input exists"""
        return len(self.buffer) > 0
        
        

class Stdout:
    def __init__(self):
        self.target = None   # where output goes

    def connect(self, target):
        """Connect stdout to another stream (pipe, stdin, terminal)"""
        self.target = target

    def write(self, data):
        if self.target:
            self.target.write(data)

    def writeline(self, data):
        self.write(data + "\n")
        
        
        
class Stderr:
    def __init__(self):
        self.target = None

    def connect(self, target):
        """Connect stderr to terminal, log, or pipe"""
        self.target = target

    def write(self, data):
        if self.target:
            self.target.write(data)

    def writeline(self, data):
        self.write(data + "\n")