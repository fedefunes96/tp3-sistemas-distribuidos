from protocol.socket import Socket
import threading
from queue import Queue, Empty

class Protocol:
    def __init__(self, my_id, port, nodes_ids):
        self.my_id = my_id
        self.port = port
        self.nodes_ids = nodes_ids
        self.connections = {}
        self.threads = []

        for node in self.nodes_ids:
            self.create_connection(node)
        
        self.listen_socket = Socket()
    
    def create_connection(self, node_id)
        sock = Socket()
        try:
            sock.connect(node, port)
            self.connections[node_id] = sock
        except SocketError:
            # We assume that the node is dead
            pass

    def start_receiving(self, callback):
        self.callback = callback

        self.listen_socket.bind(self.my_ip, self.port)

        total_cons = 0

        while True:
            self.remove_pending_connections()

            sock = self.listen_socket.accept()

            #Init a queue to coordinate thread finishing
            queue = Queue()

            conn_th = threading.Thread(
                target=self.handle_connection,
                args=(sock, callback, queue)
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

    def broadcast_message(self, msg_type):
        for node_id in self.connections():
            try:
                self.send_msg(self.connection[node_id], msg_type)

                [node_id, msg] = self.recv(self.connections[node_id])

                self.callback(node_id, msg)
            except SocketTimeout:
                # Node failed to answer, remove its socket
                conn = self.connections.pop(node_id)
                conn.close()

    def send_msg(self, sock, msg_type):
        sock.send_string(self.my_id)
        sock.send_string(msg_type)

    def recv_msg(self, sock):
        return [sock.recv_string(), sock.recv_string()]

    def handle_connection(self, sock, callback, queue):
        while True:
            try:
                [node_id, msg] = self.recv(sock)

                if node_id not in self.connections:
                    #Received connection from a node which came up
                    self.create_connection(node_id)

                command = sock.recv_string()

                if command == "Status":
                    sock.send_string("Alive")
                elif command == "Election":
            except SocketTimeout:
                #Connection broke, just stop handling this connection
                break
        
        #Ending
        queue.put_nowait(0)