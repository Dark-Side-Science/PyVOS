class BinderProxy:

    def __init__(self, connection):
        self.connection = connection

    def send_request(self, request):

        self.connection.send(request)

    def get_response(self, blocking=True):

        if blocking:
            return self.connection.recv()

        if self.connection.poll():
            return self.connection.recv()

        return None