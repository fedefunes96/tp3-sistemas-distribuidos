import pika
import sys
import random
import time
import json

from middleware.connection import Connection

from communication.message_types import NORMAL, EOF, TOP_CITIES, STOP, FINISHED


class Protocol:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue):
        self.connection = Connection()

        self.pending_connections = total_workers

        self.receiver = self.connection.create_direct_receiver(recv_queue)
        self.sender = self.connection.create_direct_sender(send_queue)
        self.status_sender = self.connection.create_direct_sender(status_queue)

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
                #self.receiver.close()
                self.receiver.close()
        elif msg_type == STOP:
            self.receiver.close()
            self.status_sender.send(FINISHED, FINISHED)
            self.sender.send(STOP, '')
        else:
            self.callback(json.loads(msg))

    def send_data(self, top_cities):
        self.sender.send(TOP_CITIES, json.dumps(top_cities))
        self.sender.send(EOF, '')
