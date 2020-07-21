from synchronization.protocol.protocol import Protocol
import random
import time
import threading
from socket import error, timeout

WAIT_TIME_PER_CHECK = [3, 6] #Seconds

class BullyLeader:
    def __init__(self, my_node, port, nodes_ids):#, callback_leader):
        self.my_node = my_node
        self.port = port
        self.nodes_ids = sorted(nodes_ids)
        self.lock = threading.Lock()
        self.last_leader = None

        self.protocol = Protocol(
            self.my_node,
            self.port,
            self.nodes_ids,
            self.new_leader
        )
        
    def new_leader(self, node):
        #Locking because an election could be raised while im processing this
        with self.lock:
            #Im the new leader
            if node == self.my_node and self.last_leader != self.my_node:
                self.callback_new_leader()
            #Someone took my role
            elif node != self.my_node and self.last_leader == self.my_node:
                self.callback_disposed_leader()

            self.last_leader = node            

    def start(self, callback_new_leader, callback_disposed_leader):
        self.callback_new_leader = callback_new_leader
        self.callback_disposed_leader = callback_disposed_leader
        #First start receiving messages
        self.protocol.start()

        #Initialize sockets
        self.protocol.initialize_connections()

        #And start a new election
        self.protocol.start_election()

        while True:
            if self.protocol.in_election:
                self.protocol.start_election()
            else:
                self.protocol.broadcast_all("Status")

            time_to_wait = random.randint(
                WAIT_TIME_PER_CHECK[0],
                WAIT_TIME_PER_CHECK[1] + 1
            )

            time.sleep(time_to_wait)

        self.protocol.join()
