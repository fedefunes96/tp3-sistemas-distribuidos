import socket

BUFFER_RECV = 128

class Socket:
    def __init__(self, sock=None, address=None, timeout=None):
        if sock == None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = sock
            self.address = address

        if timeout != None:
            self.socket.settimeout(timeout)
    
    def connect(self, ip, port):
        self.address= (ip, port)
        self.socket.connect(self.address)

    def bind(self, ip, port):
        self.address = (ip, port)
        self.socket.bind(self.address)
        self.socket.listen(1)

    def accept(self, timeout=None):
        sock, client_address = self.socket.accept()

        return Socket(sock, client_address, timeout)

    def recv_int(self):
        integer = self.socket.recv(4)

        return int.from_bytes(integer, "big")
    
    def recv_string(self):
        amount_expected = self.recv_int()

        amount_received = 0
        message = bytearray()

        while amount_received + BUFFER_RECV < amount_expected:
            bytes_recv = self.socket.recv(BUFFER_RECV)
            message += bytes_recv
            amount_received += len(bytes_recv)

        message += self.socket.recv(amount_expected - amount_received)

        return message.decode("utf-8")
    
    def send_int(self, integer):
        self.socket.sendall(integer.to_bytes(4, byteorder='big'))
    
    def send_string(self, string):
        self.send_int(len(string))
        self.socket.sendall(string.encode('utf8'))

    def close(self):
        self.socket.close()
