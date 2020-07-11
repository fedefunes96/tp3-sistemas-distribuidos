from multiprocessing import Process, Queue
from middleware.connection import Connection
from queue import Empty
from communication.message_types import STATUS, ALIVE, DEAD
import os

STATUS_QUEUE_NAME = "status_node"

class StatusChecker:
    def __init__(self, process_to_check):
        self.process = process_to_check

    def start(self):
        self.connection = Connection()

        self.receiver = self.connection.create_rpc_receiver(STATUS_QUEUE_NAME)
        self.receiver.start_receiving(self.request_received)

    def request_received(self, reply_to, cor_id, msg):
        from_where = msg
        
        if msg == STATUS:
            #Since this runs in another process
            #we will check if parent process is alive (AKA: The main process)
            if self.process.is_alive():
                self.receiver.reply(cor_id, reply_to, ALIVE)
            else:
                self.receiver.reply(cor_id, reply_to, DEAD)
