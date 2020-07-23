import pika
import sys
import random
import time

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF, STOP, READY, REQUEST_PLACES

class ProtocolInitialize:
    def __init__(self, send_queue, callback):
        self.connection = Connection()

        self.callback = callback

        self.sender = self.connection.create_rpc_sender(send_queue)

        #self.receiver = self.connection.create_topic_receiver(recv_queue)
    
    def start_connection(self):
        print("Waiting for places")
        #self.receiver.start_receiving(self.data_read)
        #self.connection.close()

        #Wait for answer
        _answer = self.sender.send(REQUEST_PLACES)
        print("Places are available")

    '''def data_read(self, msg_type, msg):
        if msg_type == STOP:
            self.receiver.close()
            return True
        elif msg_type == EOF:
            self.receiver.close()
            return False
        else:
            print("Got message: " + msg)
            [region, latitude, longitude] = msg.split(",")
            self.callback(region, float(latitude), float(longitude))
            return False

    def close(self):
        self.receiver.close()
        self.connection.close()'''
