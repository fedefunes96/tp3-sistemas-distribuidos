from middleware.connection import Connection
from communication.message_types import NORMAL, EOF

class ReceiverProtocol:
    def __init__(self, recv_queue):
        self.connection = Connection()

        self.receiver = self.connection.create_direct_receiver(recv_queue)
    
    def start_connection(self, callback, callback_eof):
        print("Starting to receive places")
        self.callback = callback
        self.callback_eof = callback_eof

        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            self.callback_eof()
        else:
            [region, latitude, longitude] = msg.split(",")
            self.callback(region, latitude, longitude)
