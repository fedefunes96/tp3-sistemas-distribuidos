import pika
import sys
import random
import time
import json

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF, STOP, READY, REQUEST_PLACES
from middleware.secure_connection.secure_rpc_sender import SecureRpcSender

class ProtocolInitialize:
    def __init__(self, send_queue, callback):
        self.connection = Connection()

        self.callback = callback

        #self.sender = self.connection.create_rpc_sender(send_queue)
        self.sender = SecureRpcSender(send_queue, self.connection)
    
    def start_connection(self):
        print("Waiting for places")

        #Wait for answer
        conn_id = self.sender.send(json.dumps([REQUEST_PLACES, ""]))
        print("Places are available")
        return conn_id
