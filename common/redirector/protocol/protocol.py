import pika
import sys
import random
import time

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF, STOP, FINISHED
from middleware.secure_connection.secure_direct_sender import SecureDirectSender
from middleware.secure_connection.secure_distributed_receiver import SecureDistributedReceiver

class Protocol:
    def __init__(self, recv_queue, send_queues, master_send_queue, status_queue):
        self.connection = Connection()
        self.receiver = SecureDistributedReceiver(recv_queue, self.connection)
        self.status_sender = SecureDirectSender(status_queue, self.connection)
        self.senders = {}

        for queue in send_queues:
            self.senders[queue] = SecureDirectSender(queue, self.connection)

        self.master_sender = SecureDirectSender(master_send_queue, self.connection  )

    def start_connection(self, callback, callback_eof):
        self.callback = callback
        self.callback_eof = callback_eof

        self.receiver.start_receiving(self.data_read)

        # self.send_master_ended()
        # self.receiver.close()
        # self.connection.close()
    
    def send_data(self, data, where):
        self.senders[where].send(NORMAL, data)
    
    def send_master_ended(self):
        self.master_sender.send(EOF, "")

    def send_master_stop(self):
        self.master_sender.send(STOP, "")

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            self.callback_eof()
            self.send_master_ended()
            print("Ended processing")
        elif msg_type == STOP:
            self.receiver.close()
            self.send_master_stop()
            self.status_sender.send(FINISHED, FINISHED)
        else:            
            self.callback(msg)
            #self.receiver.send_ack(method)
