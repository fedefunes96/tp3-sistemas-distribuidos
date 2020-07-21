'''import threading
from socket import timeout, error

class LeaderManager:
    def __init__(self, node, leader_algorithm):
        self.leader_algorithm = leader_algorithm
        self.my_node = node
        self.last_leader = None

    def start(self, new_leader_callback, roll_disposed_callback):
        self.new_leader_callback = new_leader_callback
        self.roll_disposed_callback = roll_disposed_callback

        self.leader_algorithm.start(self.new_leader_detected)

    def wait_if_disposed_node(self):
        #Wait to check if the process who i stole the leadership
        #is really dead, if not, wait until it finishes it's work
        if self.last_leader == None
            return
        
        try:
            self.leader_algorithm.send_msg_to(self.last_leader)
        except (timeout, error):


    def new_leader_detected(self, node):
        #Locking cause an election could be raised while im processing this
        with self.lock:
            #Im the new leader
            if node == self.my_node and self.last_leader != self.my_node:
                self.wait_if_disposed_node()
                self.new_leader_callback()
            #Someone took my role
            elif node != self.my_node and self.last_leader == self.my_node:
                self.roll_disposed_callback()

            self.last_leader = node'''