from middleware.connection import Connection
from communication.message_types import RESTART, REQUEST_PLACES
from middleware.secure_connection.secure_rpc_receiver import SecureRpcReceiver
from state_saver.state_saver import StateSaver
import json

class RequesterProtocol:
    def __init__(self, recv_queue, state_saver):
        self.connection = Connection()

        self.receiver = SecureRpcReceiver(recv_queue, self.connection)
        self.state_saver = state_saver

    def start_connection(self, connection_id):
        self.connection_id = connection_id

        self.receiver.start_receiving(self.data_read)

    def data_read(self, reply_to, cor_id, msg):
        [msg, conn_id] = json.loads(msg)

        print("Received msg: {}".format(msg))

        if msg == RESTART:
            if self.state_saver.is_duplicated("STATE", conn_id):
                print("Duplicated message: {}".format(conn_id))
                return
            #Close and it will be raised eternally
            self.receiver.reply(cor_id, reply_to, RESTART)

            self.state_saver.save_state("STATE", conn_id, json.dumps([self.connection_id, "RESTART"]))

            self.receiver.close()

        elif msg == REQUEST_PLACES:
            reply = self.connection_id

            self.receiver.reply(cor_id, reply_to, reply)
