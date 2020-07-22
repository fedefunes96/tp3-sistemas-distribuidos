import pika
import sys
import random
import time

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF, STOP, FINISHED

class Protocol:
    def __init__(self, recv_queue, send_queues, master_send_queue, status_queue):
        self.connection = Connection()
        self.receiver = self.connection.create_distributed_work_receiver(recv_queue)
        self.status_sender = self.connection.create_direct_sender(status_queue)
        self.senders = {}

        for queue in send_queues:
            self.senders[queue] = self.connection.create_direct_sender(queue)

        self.master_sender = self.connection.create_direct_sender(master_send_queue)

    def start_connection(self, callback, callback_eof):
        self.callback = callback
        self.callback_eof = callback_eof

        self.receiver.start_receiving(self.data_read)

        self.send_master_ended()
        self.status_sender.send(FINISHED, FINISHED)
        print("Sent finished to status checker")
        self.receiver.close()
        print("Closed receiver")
        self.connection.close()
        print("Connection closed. should return?")
    
    def send_data(self, data, where):
        self.senders[where].send(NORMAL, data)
    
    def send_master_ended(self):
        self.master_sender.send(EOF, "")

    def send_master_stop(self):
        self.master_sender.send(STOP, "")

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            self.callback_eof()
            self.receiver.close()
        elif msg_type == STOP:
            self.receiver.close()
            self.send_master_stop()
        else:            
            self.callback(msg)
            #self.receiver.send_ack(method)
