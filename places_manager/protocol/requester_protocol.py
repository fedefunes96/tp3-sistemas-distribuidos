from middleware.connection import Connection
from communication.message_types import RESTART, REQUEST_PLACES
from middleware.secure_connection.secure_rpc_receiver import SecureRpcReceiver

class RequesterProtocol:
    def __init__(self, recv_queue):
        self.connection = Connection()

        self.receiver = SecureRpcReceiver(recv_queue, self.connection)
    
    def start_connection(self, callback):
        self.callback = callback

        self.receiver.start_receiving(self.data_read)

    def data_read(self, reply_to, cor_id, msg):
        #(TODO) Duplicate filter
        if msg == RESTART:
            #Close and it will be raised eternally
            self.receiver.reply(cor_id, reply_to, RESTART)
            self.receiver.close()
        elif msg == REQUEST_PLACES:
            reply = self.callback()

            self.receiver.reply(cor_id, reply_to, reply)
