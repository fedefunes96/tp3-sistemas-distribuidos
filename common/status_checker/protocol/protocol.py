import pika

from middleware.connection import Connection
from communication.message_types import STATUS, ALIVE, DEAD
from middleware.secure_connection.secure_direct_sender import SecureDirectSender

class Protocol:
    def __init__(self, send_queue):
        self.connection = Connection()

        self.sender = SecureDirectSender(send_queue, self.connection)

    def send_status(self, status, worker_id, worker_type):
        msg = status + "," + worker_id + "," + worker_type
        self.sender.send(STATUS, msg)
