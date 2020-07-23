from middleware.connection import Connection
from communication.message_types import RESTART, REQUEST_PLACES

class RequesterProtocol:
    def __init__(self, recv_queue):
        self.connection = Connection()

        self.receiver = self.connection.create_rpc_receiver(recv_queue)
    
    def start_connection(self, callback):
        self.callback = callback

        self.receiver.start_receiving(self.data_read)

    def data_read(self, reply_to, cor_id, msg):
        if msg == RESTART:
            #Close and it will be raised eternally
            self.receiver.close()
            self.receiver.reply(cor_id, reply_to, RESTART)
        elif msg == REQUEST_PLACES:
            reply = self.callback()

            self.receiver.reply(cor_id, reply_to, reply)
