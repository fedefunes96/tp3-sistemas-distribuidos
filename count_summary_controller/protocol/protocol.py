import pika
import sys
import random
import time
import json

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF, TOTAL_COUNT

class Protocol:
    def __init__(self, recv_queue, send_queue):
        self.connection = Connection()
        self.receiver = self.connection.create_direct_receiver(recv_queue)
        self.sender = self.connection.create_direct_sender(send_queue)

    def start_connection(self, callback):
        self.callback = callback
        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            self.receiver.close()
        else:
            [positivi, deceduti] = msg.split(',')
            self.callback(int(positivi), int(deceduti))

    def send_data(self, percentage):
        self.sender.send(TOTAL_COUNT, str(percentage))
        self.sender.send(EOF, '')