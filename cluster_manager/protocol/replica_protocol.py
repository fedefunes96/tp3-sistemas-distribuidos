from middleware.connection import Connection
from communication.message_types import APPEND, WRITE, WRITE_OK, FAILED
from middleware.secure_connection.secure_rpc_receiver import SecureRpcReceiver
import json

class ReplicaProtocol:
    def __init__(self, recv_queue):
        self.connection = Connection()
                  
        self.receiver = SecureRpcReceiver(recv_queue, self.connection)

    def start_receiving(self, callback_app, callback_wr):
        self.callback_app = callback_app
        self.callback_wr = callback_wr

        self.receiver.restart_queue()
        self.receiver.start_receiving(self.data_read)

    def data_read(self, reply_to, cor_id, msg):
        #[folder_to_read, file_to_read, data, mode] = msg.split('@@')
        [folder_to_read, file_to_read, data, mode] = json.loads(msg)

        if mode == APPEND:
            reply = self.callback_app(folder_to_read, file_to_read, data)
            self.receiver.reply(cor_id, reply_to, reply)
        elif mode == WRITE:
            reply = self.callback_wr(folder_to_read, file_to_read, data)
            reply = WRITE_OK
            print("Replying to writer: {}".format(reply))
            self.receiver.reply(cor_id, reply_to, reply)
            print("Replied successfully")
