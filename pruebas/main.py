#!/usr/bin/env python3
from middleware.connection import Connection
from middleware.secure_connection.secure_rpc_sender import SecureRpcSender
from middleware.secure_connection.secure_rpc_receiver import SecureRpcReceiver
from multiprocessing import Process

class Client:
    def __init__(self):
        connection = Connection()

        self.server_sender = SecureRpcSender("server_1_dir", connection)
    
    def start(self):
        msg = "Hola servidor"
        print("[CLIENTE] Enviando al servidor {}".format(msg))
        response = self.server_sender.send(msg)

        print(response) 

class Server_a:
    def __init__(self):
        connection = Connection()

        self.server_receiver = SecureRpcReceiver("server_1_dir", connection)
        self.server_sender = SecureRpcSender("server_2_dir", connection)
    
    def start(self):
        self.server_receiver.start_receiving(self.data_read)
    
    def data_read(self, reply_to, cor_id, msg):
        print("[SERVER_INTERMEDIO] Cliente me envio: {}".format(msg))

        response = self.server_sender.send(msg)

        print("[SERVER_INTERMEDIO] Servidor intermedio recibio: {}".format(response))

        self.server_receiver.reply(cor_id, reply_to, response)

        print("[SERVER_INTERMEDIO] Ya respondi al cliente")

class Server_b:
    def __init__(self):
        connection = Connection()

        self.server_receiver = SecureRpcReceiver("server_2_dir", connection)
    
    def start(self):
        self.server_receiver.start_receiving(self.data_read)
    
    def data_read(self, reply_to, cor_id, msg):
        print("[SERVER_FINAL] Servidor intermedio me envio: {}".format(msg))

        response = "Hola cliente"

        self.server_receiver.reply(cor_id, reply_to, response)

        print("[SERVER_FINAL] Ya respondi al servidor intermedio")

def server_2():
    server = Server_b()

    server.start()

def server_1():
    server = Server_a()

    server.start()

def client():
    client = Client()

    client.start()     

def main():
    print("Empezando las pruebas")
    p1 = Process(target=client)
    p1.start()

    p2 = Process(target=server_1)
    p2.start()

    p3 = Process(target=server_2)
    p3.start()

    p1.join()
    p2.join()
    p3.join()

if __name__ == "__main__":
    main()
