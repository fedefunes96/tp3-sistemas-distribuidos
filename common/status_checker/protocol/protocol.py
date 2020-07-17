import pika

from middleware.connection import Connection
from communication.message_types import STATUS, ALIVE, DEAD

class Protocol:
    def __init__(self, send_queue):
        self.connection = Connection()

        self.sender = self.connection.create_direct_sender(send_queue)

    def send_data(self, status, worker_id, worker_type):
        msg = status + "," + worker_id + "," + worker_type
        self.sender.send(STATUS, msg)
