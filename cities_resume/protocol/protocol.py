import pika
import sys
import random
import time
import json

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF

class Protocol:
    def __init__(self, recv_queue, send_queue, master_queue):
        self.connection = Connection()
        self.receiver = self.connection.create_direct_receiver(recv_queue)
        self.sender = self.connection.create_direct_sender(send_queue)
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
            #self.receiver.close()
            print("Ended processing")
            self.callback_eof()
        else:
            self.callback(msg)
