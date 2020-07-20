from protocol.protocol import Protocol
from protocol.exceptions import TimeoutRequest
import time
#import threading

WAIT_PER_REQUEST = 3 # 3 Seconds

class TokenRingLeader:
    def __init__(self, my_id, ids_ordered):
        self.my_id = my_id
        self.ids_ordered = ids_ordered

        self.next_node = self.get_next_node(self.my_id)

        self.protocol = Protocol(self.next_node)

        self.leader = max(self.ids_ordered)
        self.in_election = False
        self.working = True
    
    def msg_received(self, msg_type, msg):
        if msg_type == "Status":
            pass
            #self.protocol.send_status_check()
        elif msg_type == "Election":
            self.election_received(msg)
        elif msg_type == "Leader":
            self.leader_received(msg)

    def leader_received(self, node_id):
        self.leader = node_id
        self.in_election = False        

    def election_received(self, nodes_ids):
        # Select new leader
        if self.my_id in nodes_ids:
            self.leader = max(nodes_ids)
            self.send_new_leader(self.leader)
        elif not self.in_election:
            self.send_election(nodes_ids + self.my_id)

    def start(self):
        self.protocol.start_receiving(self.msg_received)

        while self.working:
            try:
                '''if self.im_leader():
                    self.protocol.send_status_check()
                    self.protocol.wait_message(self.msg_received)
                else:
                    self.protocol.wait_message(self.msg_received)'''
                self.protocol.send_status_check()
                time.sleep(WAIT_PER_REQUEST)
            except TimeoutRequest:
                # Next node is dead, change it
                self.change_dead_node()

                #All nodes are dead except myself, stop sending status, good luck
                if not self.continue_working:
                    self.working = False
                    self.leader = self.my_id
                    break

                self.protocol.change_direction(self.next_node)

                #If dead node was leader, start election if not in election
                if self.dead_node == self.leader and not self.in_election:
                    self.start_election()

        self.protocol.join()
    
    def start_election(self):
        self.send_election(self.my_id, [self.my_id])

    def send_election(self, nodes_ids):
        self.in_election = True

        try:
            self.protocol.send_start_election(nodes_ids)
        except TimeoutRequest:
            # Next node is dead, change it
            self.change_dead_node()

            #All nodes are dead except myself, stop sending status, good luck
            if not self.continue_working:
                self.in_election = False
                self.working = False
                self.leader = self.my_id
                return
            
            self.protocol.change_direction(self.next_node)
    
    def send_new_leader(self, node_id):
        self.in_election = False

        try:
            self.protocol.send_new_leader(node_id)
        except TimeoutRequest:
            # Next node is dead, change it
            self.change_dead_node()

            #All nodes are dead except myself, stop sending status, good luck
            if not self.continue_working:
                self.working = False
                self.leader = self.my_id
                return
            
            self.protocol.change_direction(self.next_node)        

    def im_leader(self):
        return self.leader == self.my_id

    def change_dead_node(self):
        self.dead_node = self.next_node
        self.next_node = self.get_next_node(self.next_node)

    def continue_working(self):
        return self.next_node != self.my_id:

    def get_next_node(self, from_node):
        return self.ids_ordered[
            (self.ids_ordered.index(self.from_node) + 1) % len(self.ids_ordered)
        ]
