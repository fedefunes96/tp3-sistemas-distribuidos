import threading

class LeaderManager:
    def __init__(self, node, leader_algorithm):
        self.leader_algorithm = leader_algorithm
        self.my_node = node
        self.last_leader = None
        self.lock = threading.Lock()

    def start(self, new_leader_callback, roll_disposed_callback):
        self.new_leader_callback = new_leader_callback
        self.roll_disposed_callback = roll_disposed_callback

        self.leader_algorithm.start(self.new_leader_detected)

    def new_leader_detected(self, node):
        #Locking cause an election could be raised while im processing this
        with lock:
            #Im the new leader
            if node == self.my_node and self.last_leader != self.my_node:
                self.new_leader_callback()
            #Someone took my role
            elif node != self.my_node and self.last_leader = self.my_node:
                self.roll_disposed_callback()

            self.last_leader = node