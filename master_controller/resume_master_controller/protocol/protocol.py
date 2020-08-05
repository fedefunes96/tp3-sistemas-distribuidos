from middleware.connection import Connection

from communication.message_types import NORMAL, EOF, STOP, FINISHED
from middleware.secure_connection.secure_direct_sender import SecureDirectSender
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver

class Protocol:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue):
        self.connection = Connection()

        self.total_workers = total_workers
        self.pending_connections = total_workers
        self.receiver = SecureDirectReceiver(recv_queue, self.connection)
        self.sender = SecureDirectSender(send_queue, self.connection)
        self.status_sender = SecureDirectSender(status_queue, self.connection)

        self.send_queue = send_queue

    def start_connection(self):
        self.receiver.start_receiving(self.data_read)
        self.connection.close()

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            self.pending_connections -= 1
            if self.pending_connections == 0:
                print("Ended processing {}".format(msg))
                self.sender.send(EOF, msg)
                self.pending_connections = self.total_workers
        elif msg_type == STOP:
            self.receiver.close()
            self.sender.send(STOP, '')
            self.status_sender.send(FINISHED, FINISHED)

