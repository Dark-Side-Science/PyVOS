class BinderProxy:

    def __init__(self, conn, package):
        self.conn = conn
        self.package = package

    def send_request(self, request):
        if not request:
            return
        self.conn.send(self.package + "|" + request)

    def get_response(self, blocking=True):
        if blocking:
            return self.conn.recv()

        if self.conn.poll(0.01):
            return self.conn.recv()

        return None