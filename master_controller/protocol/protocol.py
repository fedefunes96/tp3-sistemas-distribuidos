from middleware.connection import Connection

from communication.message_types import EOF, STOP, FINISHED


class Protocol:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue):
        self.connection = Connection()
        print("Connected to RabbitMQ")

        self.total_workers = total_workers

        self.status_sender = self.connection.create_distributed_work_sender(status_queue)
        self.receiver = self.connection.create_direct_receiver(recv_queue)
        self.sender = self.connection.create_distributed_work_sender(send_queue)

    def start_connection(self):
        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        print("Got a message!")
        if msg_type == STOP:
            self.send_stop()
            self.status_sender.send(FINISHED, FINISHED)
            self.close()
        elif msg_type == EOF:
            self.send_eof()

    def send_eof(self):
        for i in range(0, self.total_workers):
            self.sender.send(EOF, '')

    def send_stop(self):
        for i in range(0, self.total_workers):
            self.sender.send(STOP, '')

    def close(self):
        self.receiver.close()
        self.connection.close()
