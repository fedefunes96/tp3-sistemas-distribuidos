import pika
import sys
import random
import time
import json

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF, STOP, FINISHED

class Protocol:
    def __init__(self, recv_queue, send_queue, master_queue, status_queue):
        self.connection = Connection()
        self.receiver = self.connection.create_direct_receiver(recv_queue)
        self.sender = self.connection.create_direct_sender(send_queue)
        self.status_sender = self.connection.create_direct_sender(status_queue)
        self.master_sender = self.connection.create_direct_sender(master_queue)

    def start_connection(self, callback, callback_eof):
        self.callback = callback
        self.callback_eof = callback_eof
        self.receiver.start_receiving(self.data_read)

    def send_data(self, data):
        self.sender.send(NORMAL, json.dumps(data))

        self.sender.send(EOF, "")
        #self.master_sender.send(EOF, "")

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            print("Ended processing")
            self.callback_eof()
        elif msg_type == STOP:
            self.receiver.close()
            self.sender.send(STOP, "")
            self.master_sender.send(STOP, "")
            self.status_sender.send(FINISHED, FINISHED)
        else:
            [date, result] = msg.split(',')
            self.callback(date, result)
