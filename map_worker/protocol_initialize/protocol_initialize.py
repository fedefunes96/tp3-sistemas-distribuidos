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
    
    def start_connection(self):
        print("Waiting for places")

        #Wait for answer
        conn_id = self.sender.send(REQUEST_PLACES)
        print("Places are available")
        return conn_id
