class SecureSender:
    def __init__(self, queue, connection):
        self.queue = queue
        self.connection = connection

    def send(self, msg_type, msg):
        sent = False

        while not sent:
            try:
                self.sender = self.create_channel()
                self.sender.send(msg_type, msg)
                sent = True
            except Exception as e:
                print(e)
                self.connection.force_connect()

    def create_channel(self):
        raise NotImplementedError
