import pika
import sys
import random
import time
import json

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF, STOP, FINISHED
from middleware.secure_connection.secure_direct_sender import SecureDirectSender
from middleware.secure_connection.secure_distributed_receiver import SecureDistributedReceiver

class Protocol:
    def __init__(self, recv_queue, send_queues, master_send_queue, status_queue, state_saver, my_id):
        self.connection = Connection()
        self.status_sender = SecureDirectSender(status_queue, self.connection)
        self.senders = {}

        self.recv_queue = recv_queue

        for queue in send_queues:
            self.senders[queue] = SecureDirectSender(queue, self.connection)

        self.master_sender = SecureDirectSender(master_send_queue, self.connection)
        self.state_saver = state_saver
        self.my_id = my_id

    def start_connection(self, callback, callback_eof):
        self.callback = callback
        self.callback_eof = callback_eof

        self.receiver = SecureDistributedReceiver(self.recv_queue, self.connection)

        self.receiver.start_receiving(self.data_read)
    
    def send_data(self, data, where):
        self.senders[where].send(NORMAL, data)
    
    def send_master_ended(self, msg):
        data_recv = json.loads(msg)
        #[conn_id, msg_id, eof] => [conn_id, my_id, eof]
        data_recv[1] = self.my_id

        self.master_sender.send(EOF, json.dumps(data_recv))

    def send_master_stop(self):
        self.master_sender.send(STOP, "")

    def data_read(self, msg_type, msg):
        if msg_type == STOP:
            self.receiver.close()
            self.send_master_stop()
            self.status_sender.send(FINISHED, FINISHED)
            return

        if msg_type == EOF:
            data_recv = json.loads(msg)
            [connection_id, message_id] = data_recv[:2]

            if self.state_saver.is_duplicated("STATE", connection_id):
                print("Duplicated message: {}".format(connection_id))
                return

            self.callback_eof(msg)
            self.send_master_ended(msg)

            print("Ended processing")
            self.state_saver.save_state("STATE", connection_id, "WAITING")
            self.receiver.close()
        else:
            print("Received MESSSS: {}".format(msg))
            self.callback(msg)
