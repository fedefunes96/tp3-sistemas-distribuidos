import pika
import sys
import random
import time
import json

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF, DATE_RESULTS

class Protocol:
    def __init__(self, recv_queue, send_queue, total_workers):
        self.connection = Connection()

        self.pending_connections = total_workers

        self.receiver = self.connection.create_direct_receiver(recv_queue)
        self.sender = self.connection.create_direct_sender(send_queue)

    def start_connection(self, callback):
        self.callback = callback
        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            #self.receiver.close()
            self.pending_connections -= 1

            if self.pending_connections == 0:
                self.receiver.close()   
        else:
            self.callback(json.loads(msg))

    def send_data(self, date_data):
        self.sender.send(DATE_RESULTS, json.dumps(date_data))
        self.sender.send(EOF, '')
