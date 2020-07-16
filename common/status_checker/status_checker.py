from multiprocessing import Process, Queue
from middleware.connection import Connection
from queue import Empty
from communication.message_types import STATUS, ALIVE, DEAD
import os
import time
from random import randrange

RANGE_WAIT_STATUS = [5, 15]

class StatusChecker:
    def __init__(self, worker_id, worker_type, processes_to_check, queue):
        self.processes = processes_to_check
        self.queue = queue

    def start(self):
        connection = Connection()
        sender = self.connection.create_direct_sender(self.queue)

        while True:
            randrange(RANGE_WAIT_STATUS[0], RANGE_WAIT_STATUS[1], 1)

            self.send_status(sender)
        #self.receiver = self.connection.create_rpc_receiver(self.queue)
        #self.receiver.start_receiving(self.request_received)

    def send_status(self, sender):
        if self.all_processes_alive(self.processes):
            sender.send(STATUS, ALIVE)
        else:
            sender.send(STATUS, DEAD)

    def request_received(self, reply_to, cor_id, msg):
        from_where = msg
        
        if msg == STATUS:            
            if self.all_processes_alive(self.processes):
                self.receiver.reply(cor_id, reply_to, ALIVE)
            else:
                self.receiver.reply(cor_id, reply_to, DEAD)

    def all_processes_alive(self, processes):
        for p in processes:
            if not p.is_alive():
                return False

        return True
