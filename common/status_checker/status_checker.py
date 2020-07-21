from multiprocessing import Process, Queue
from middleware.connection import Connection
from queue import Empty
from communication.message_types import STATUS, ALIVE, DEAD, FINISHED
import os

class StatusChecker:
    def __init__(self, processes_to_check, queue):
        self.processes = processes_to_check
        self.queue = queue

    def start(self):
        self.connection = Connection()

        self.receiver = self.connection.create_rpc_receiver(self.queue)
        self.receiver.start_receiving(self.request_received)

    def request_received(self, reply_to, cor_id, msg):
        from_where = msg
        
        if msg == STATUS:
            all_alive = True
            
            if self.all_processes_alive(self.processes):
                self.receiver.reply(cor_id, reply_to, ALIVE)
            else:
                self.receiver.reply(cor_id, reply_to, DEAD)
        elif msg == FINISHED:
            print("Got a FINISHED")
            # self.receiver.reply(cor_id, reply_to, FINISHED)
            self.receiver.close()

    def all_processes_alive(self, processes):
        for p in processes:
            if not p.is_alive():
                return False

        return True
