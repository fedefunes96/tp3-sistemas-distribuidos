class SecureReceiver:
    def __init__(self, queue, connection):
        self.queue = queue
        self.connection = connection
        self.receiver = None

    def start_receiving(self, data_read):
        receiving = True

        while receiving:
            try:
                self.receiver = self.create_channel()
                self.receiver.start_receiving(data_read)
                receiving = False
            except Exception as e:
                print(e)
                self.connection.force_connect()

    def create_channel(self):
        raise NotImplementedError

    def close(self):
        self.receiver.close()
