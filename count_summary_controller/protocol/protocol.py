import pika
import sys
import random
import time
import json

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF, TOTAL_COUNT, STOP, FINISHED
from middleware.secure_connection.secure_direct_sender import SecureDirectSender
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver

class Protocol:
    def __init__(self, recv_queue, send_queue, status_queue):
        self.connection = Connection()
        self.receiver = SecureDirectReceiver(recv_queue, self.connection)
        self.sender = SecureDirectSender(send_queue, self.connection)
        self.status_sender = SecureDirectSender(status_queue, self.connection)

    def start_connection(self, callback, callback_eof):
        self.callback = callback
        self.callback_eof = callback_eof
        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            print("Ended processing")
            self.callback_eof()
        elif msg_type == STOP:
            self.receiver.close()
            self.sender.send(STOP, '')
            self.status_sender.send(FINISHED, FINISHED)
        else:
            self.callback(msg)

    def send_data(self, msg):
        self.sender.send(TOTAL_COUNT, msg)
        self.sender.send(EOF, '')