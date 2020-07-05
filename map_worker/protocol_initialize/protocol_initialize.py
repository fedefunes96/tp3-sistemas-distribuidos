import pika
import sys
import random
import time

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF

class ProtocolInitialize:
    def __init__(self, recv_queue, callback):
        self.connection = Connection()

        self.callback = callback

        self.receiver = self.connection.create_topic_receiver(recv_queue)
    
    def start_connection(self):
        print("Starting to receive places")
        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            self.connection.close()
        else:
            [region, latitude, longitude] = msg.split(",")
            self.callback(region, float(latitude), float(longitude))
