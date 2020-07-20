from protocol.socket import Socket
from socket import error, timeout
import threading
from queue import Queue, Empty
import time

WAIT_NEW_ELECTION = 30 #In seconds
TIMEOUT_SOCKET = 10 #In seconds

class Protocol:
    def __init__(self, my_id, port, nodes_ids, callback_newleader, callback_timer):
        self.my_id = my_id
        self.port = port
        self.nodes_ids = nodes_ids
        self.connections = {}
        self.threads = []
        self.callback_newleader = callback_newleader
        self.callback_timer = callback_timer

        self.leader = None
        self.in_election = False

        self.timer = False

        for node in self.nodes_ids:
            self.create_connection(node)
        
        self.listen_socket = Socket(timeout=TIMEOUT_SOCKET)
    
    def create_connection(self, node_id)
        sock = Socket(timeout=TIMEOUT_SOCKET)
        try:
            sock.connect(node, port)
            self.connections[node_id] = sock
        except error:
            #We assume that the node is dead
            #If there was no leader, start election
            if node_id == self.leader:
                self.start_election()

    def start_receiving(self):
        self.listen_socket.bind(self.my_ip, self.port)

        total_cons = 0

        while True:
            self.remove_pending_connections()

            sock = self.listen_socket.accept()

            #Init a queue to coordinate thread finishing
            queue = Queue()

            conn_th = threading.Thread(
                target=self.handle_connection,
                args=(sock, queue)
            )

            self.threads.append((total_cons, conn_th, queue))

            total_cons += 1

    def remove_pending_connections(self):
        to_remove = []
        for conn_id, conn_th, queue in self.threads:
            try:
                _tmp = queue.get_nowait()
                to_remove.append(conn_id)
                conn_th.join()
            except Empty:
                pass
        
        self.threads = [x for x in self.threads if x[0] not in to_remove]

    def broadcast_message(self, nodes, msg_type):
        total_responses = 0

        for node_id in nodes:
            try:
                self.send_msg(self.connection[node_id], msg_type)

                self.handle_reply(self.connection[node_id])

                total_responses += 1
            except timeout:
                #Node failed to answer, remove its socket
                #If it was the leader or there was no leader, start election
                conn = self.connections.pop(node_id)
                conn.close()
                
                if node_id == self.leader:# and not self.in_election:
                    self.start_election()
        
        return total_responses
    
    def start_election(self):
        nodes = []

        for node_id in self.connections():
            if node_id < self.my_id:
                continue

            nodes.append(node_id)

        total_responses = self.broadcast_message(nodes, "Election")

        if total_responses == 0:
            self.leader = node_id
            self.callback_newleader(node_id)
            self.broadcast_message(self.nodes_ids, "Leader")
        else:
            self.timer = True
            #Wait to see if new leader is elected, if not, start new election
            time.sleep(WAIT_NEW_ELECTION)
            
            #No leader selected, start new election
            if self.timer == True:
                self.start_election()

        #self.in_election = False

    def handle_reply(self, sock):
        [node_id, cmd] = self.recv_msg(sock)

        if node_id not in self.connections:
            #Received connection from a node which came up
            self.create_connection(node_id)

        #Commands for replying msg
        if command == "Status":
            pass
            #self.send_msg(sock, "Alive")
        elif command == "Election":
            pass
            #self.send_msg(sock, "Ack")
            #self.in_election = True
        elif command == "Leader":
            self.leader = node_id
            self.timer = False
            self.callback_newleader(node_id)
        #Commands for sending msg
        #elif 
        #elif command == "Alive":
        #    pass
        

    def send_msg(self, sock, msg_type):
        sock.send_string(self.my_id)
        sock.send_string(msg_type)

    def recv_msg(self, sock):
        return [sock.recv_string(), sock.recv_string()]

    def handle_connection(self, sock, queue):
        while True:
            try:
                self.handle_reply(sock)
            except timeout:
                #Connection broke, just stop handling this connection
                break
        
        queue.put_nowait(0)
