import pika
import sys
import random
import time

from middleware.connection import Connection

from communication.message_types import NORMAL, EOF, TOP_CITIES, STOP, FINISHED
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver
from middleware.secure_connection.secure_direct_sender import SecureDirectSender

class Protocol:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue):
        self.connection = Connection()

        self.pending_connections = total_workers

        self.receiver = SecureDirectReceiver(recv_queue, self.connection)
        self.sender = SecureDirectSender(send_queue, self.connection)
        self.status_sender = SecureDirectSender(status_queue, self.connection)

    def start_connection(self, callback, callback_eof):
        self.callback = callback
        self.callback_eof = callback_eof
        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            # self.receiver.close()
            self.pending_connections -= 1

            if self.pending_connections == 0:
                self.callback_eof()
                print("Ended processing")
                # self.receiver.close()
                self.receiver.close()
        elif msg_type == STOP:
            self.receiver.close()
            self.status_sender.send(FINISHED, FINISHED)
            self.sender.send(STOP, '')
        else:
            self.callback(msg)

    def send_data(self, data):
        self.sender.send(TOP_CITIES, data)
        self.sender.send(EOF, '')
