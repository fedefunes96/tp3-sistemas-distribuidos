from protocol.protocol import Protocol
import random
import time

WAIT_TIME_PER_CHECK = [3, 6] #Seconds

class BullyLeader:
    def __init__(self, my_id, port, nodes_ids):
        self.my_id = my_id
        self.port = port
        self.nodes_ids = sorted(nodes_ids)

        self.protocol = Protocol(
            self.my_id,
            self.port,
            self.nodes_ids,
            self.new_leader
        )

    def new_leader(self, node_id):
        self.leader = node_id

    def start(self):
        #First start receiving messages
        self.protocol.start()

        while True:
            self.protocol.broadcast_all("Status")

            time_to_wait = random.randint(
                WAIT_TIME_PER_CHECK[0],
                WAIT_TIME_PER_CHECK[1] + 1
            )

            time.sleep(time_to_wait)

        self.protocol.join()
