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

    def msg_received(self, msg_type, msg):
        if msg_type == "Status":
            self.protocol
            #self.protocol.send_status_check()
        elif msg_type == "Election":
            self.election_received(msg)
        elif msg_type == "Leader":
            self.leader_received(msg)

    def leader_received(self, node_id):
        self.leader = node_id
        self.in_election = False        

    def election_received(self, node_id):
        if node_id
        # Select new leader
        if self.my_id in nodes_ids:
            self.leader = max(nodes_ids)
            self.send_new_leader(self.leader)
        elif not self.in_election:
            self.send_election(nodes_ids + self.my_id)

    def start(self):
        #Start receiving messages
        self.protocol.start_receiving(self.msg_received)
        #First start with an election
        self.start_election()