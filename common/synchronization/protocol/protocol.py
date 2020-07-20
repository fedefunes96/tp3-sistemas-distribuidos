from synchronization.protocol.socket import Socket
from socket import error, timeout
import threading
from queue import Queue, Empty
import time

WAIT_NEW_ELECTION = 20 #In seconds
TIMEOUT_SOCKET = 40 #In seconds
WAIT_CONNECT = 2 #In seconds
RETRY_CONNECTS = 3

class Protocol(threading.Thread):
    def __init__(self, my_id, port, nodes_ids, callback_newleader):
        super(Protocol, self).__init__()
        self.my_id = my_id
        self.port = port
        self.nodes_ids = nodes_ids
        self.connections = {}
        self.threads = []
        self.callback_newleader = callback_newleader

        self.leader = None
        self.in_election = True

        self.timer = False
        
        self.listen_socket = Socket()
    
    def initialize_connections(self):
        print("Creating all connections")
        for node in self.nodes_ids:
            self.create_connection(node)  
    
    def create_connection(self, node_id):
        if node_id in self.connections:
            return
        
        sock = Socket(timeout=TIMEOUT_SOCKET)
        attemps_to_connect = RETRY_CONNECTS
        connected = False

        while (connected == False):
            try:
                sock.connect(node_id, self.port)
                self.connections[node_id] = sock
                connected = True
            except error:
                #Retry at least RETRY_CONNECTS times
                attemps_to_connect -= 1
                time.sleep(WAIT_CONNECT)
                #We assume that the node is dead
                #If there was no leader, start election
                if attemps_to_connect > 0:
                    continue

                print("Error on connecting to: {}".format(node_id))
                if node_id == self.leader:
                    print("Error on connecting to leader: {}".format(node_id))
                    self.start_election()
                
                break

    def run(self):
        self.start_receiving()

    def start_receiving(self):
        print("Starting to receive msgs")
        self.listen_socket.bind(self.my_id, self.port)

        total_cons = 0

        while True:
            self.remove_pending_connections()

            sock = self.listen_socket.accept(5*TIMEOUT_SOCKET)

            print("New connection accepted")

            #Init a queue to coordinate thread finishing
            queue = Queue()

            conn_th = threading.Thread(
                target=self.handle_connection,
                args=(sock, queue)
            )

            conn_th.start()

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

        if len(to_remove) > 0:
            print("Removing dangling connection")
        
        self.threads = [x for x in self.threads if x[0] not in to_remove]

    def broadcast_all(self, msg_type):
        self.broadcast_message([*self.connections], msg_type)

    def broadcast_message(self, nodes, msg_type):
        total_responses = 0

        print("Sending message: {} to {}".format(msg_type, nodes))

        for node_id in nodes:
            try:
                self.send_msg(self.connections[node_id], msg_type)

                #self.handle_reply(self.connections[node_id])

                total_responses += 1
            except timeout:
                #Node failed to answer, remove its socket
                #If it was the leader or there was no leader, start election
                conn = self.connections.pop(node_id)
                conn.close()

                print("Timeout on node: {}".format(node_id))
                
                if node_id == self.leader:# and not self.in_election:
                    print("Timeout on leader node: {}".format(node_id))
                    self.start_election()
        
        return total_responses
    
    def start_election(self):
        print("Starting new election")
        nodes = []

        for node_id in self.connections:
            if node_id < self.my_id:
                continue

            nodes.append(node_id)

        total_responses = self.broadcast_message(nodes, "Election")

        if total_responses == 0:
            print("No one answered, im the new leader: {}".format(self.my_id))
            self.in_election = False
            self.leader = self.my_id
            self.callback_newleader(self.my_id)
            self.broadcast_message([*self.connections], "Leader")
        else:
            self.timer = True
            print("Someone receiving my election, wait")
            #Wait to see if new leader is elected, if not, start new election
            time.sleep(WAIT_NEW_ELECTION)
            
            #No leader selected, start new election
            #if self.timer == True:
            if self.in_election == True:
                print("No leader selected, start again")
                self.start_election()

        #self.in_election = False

    def handle_reply(self, sock):
        [node_id, cmd] = self.recv_msg(sock)

        if node_id not in self.nodes_ids:
            return

        #print("Reply to: {} {}".format(node_id, cmd))

        if node_id not in self.connections:
            #Received connection from a node which came up
            print("Received connection from {}".format(node_id))
            self.create_connection(node_id)

        #Commands for replying msg
        if cmd == "Status":
            print("Received status from: {}".format(node_id))
            pass
            #self.send_msg(sock, "Alive")
        elif cmd == "Election":
            print("Received election from: {}".format(node_id))
            #self.send_msg(sock, "Ack")
            self.in_election = True
        elif cmd == "Leader":
            print("Received new leader: {}".format(node_id))
            self.leader = node_id
            self.timer = False
            self.callback_newleader(node_id)
            self.in_election = False
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
                print("Receiver broke, who sends me died")
                break
        
        queue.put_nowait(0)
