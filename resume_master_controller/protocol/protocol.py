from middleware.connection import Connection

from communication.message_types import NORMAL, EOF, STOP, FINISHED

class Protocol:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue):
        self.connection = Connection()

        self.pending_connections = total_workers
        self.receiver = self.connection.create_direct_receiver(recv_queue)
        self.sender = self.connection.create_direct_sender(send_queue)
        self.status_sender = self.connection.create_direct_sender(status_queue)

        self.send_queue = send_queue

    def start_connection(self):
        self.receiver.start_receiving(self.data_read)
        self.connection.close()

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            self.pending_connections -= 1
            if self.pending_connections == 0:
                self.receiver.close()
            self.sender.send(EOF, '')
        elif msg_type == STOP:
            self.receiver.close()
            self.sender.send(STOP, '')
            self.status_sender.send(FINISHED, FINISHED)

