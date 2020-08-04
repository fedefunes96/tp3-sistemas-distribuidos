from middleware.connection import Connection

from communication.message_types import EOF, STOP, FINISHED
from middleware.secure_connection.secure_direct_sender import SecureDirectSender
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver
from middleware.secure_connection.secure_distributed_sender import SecureDistributedSender

class Protocol:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue):
        self.connection = Connection()
        print("Connected to RabbitMQ")

        self.total_workers = total_workers

        self.status_sender = SecureDirectSender(status_queue, self.connection)
        self.receiver = SecureDirectReceiver(recv_queue, self.connection)
        self.sender = SecureDistributedSender(send_queue, self.connection)

    def start_connection(self):
        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        print("Got a message!")
        if msg_type == STOP:
            self.send_stop()
            self.status_sender.send(FINISHED, FINISHED)
            self.close()
        elif msg_type == EOF:
            self.send_eof(msg)

    def send_eof(self, msg):
        print("Sending EOF to workers: {}".format(msg))
        for i in range(0, self.total_workers):
            self.sender.send(EOF, msg)

    def send_stop(self):
        for i in range(0, self.total_workers):
            self.sender.send(STOP, '')

    def close(self):
        self.receiver.close()
        self.connection.close()
