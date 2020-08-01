from middleware.connection import Connection
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver

class Protocol:
    def __init__(self, recv_queue):
        self.connection = Connection()

        self.receiver = SecureDirectReceiver(recv_queue, self.connection)
    
    def start_receiving(self, callback):
        self.callback = callback
        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        [status, worker_id, worker_type] = msg.split(',')

        self.callback(status, worker_id, worker_type)
