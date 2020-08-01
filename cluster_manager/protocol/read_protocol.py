from middleware.connection import Connection
from middleware.secure_connection.secure_rpc_receiver import SecureRpcReceiver

class ReadProtocol:
    def __init__(self, recv_queue):
        self.connection = Connection()
            
        self.receiver = SecureRpcReceiver(recv_queue, self.connection)
        
    def start_receiving(self, callback):
        self.callback = callback

        self.receiver.start_receiving(self.data_read)

    def data_read(self, reply_to, cor_id, msg):
        [folder_to_read, file_to_read] = msg.split('@@')

        reply = self.callback(folder_to_read, file_to_read)

        self.receiver.reply(cor_id, reply_to, reply)
