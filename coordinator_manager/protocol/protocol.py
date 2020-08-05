from middleware.connection import Connection
from communication.message_types import READY, NEW_CLIENT, RESTART
from middleware.secure_connection.secure_rpc_receiver import SecureRpcReceiver
from middleware.secure_connection.secure_direct_sender import SecureDirectSender

import json

class Protocol:
    def __init__(self, recv_queue, send_queues, state_saver):
        self.connection = Connection()
                  
        self.receiver = SecureRpcReceiver(recv_queue, self.connection)

        self.senders = []
        self.state_saver = state_saver

        for queue in send_queues:
            self.senders.append(SecureDirectSender(queue, self.connection))

    def start_receiving(self, callback_restart, callback_new_client):
        self.callback_restart = callback_restart
        self.callback_new_client = callback_new_client

        self.receiver.start_receiving(self.data_read)

    def data_read(self, reply_to, cor_id, msg):
        [conn_id, msg_type] = json.loads(msg)
        print("Received {}".format(msg))

        if self.state_saver.is_duplicated("STATE", conn_id):
            print("Duplicated message: {}".format(conn_id))
            return

        if msg_type == RESTART:
            self.callback_restart(conn_id)
            self.receiver.reply(cor_id, reply_to, READY)
            self.state_saver.save_state("STATE", conn_id, json.dumps([conn_id, "RESTART"]))
        elif msg_type == NEW_CLIENT:
            reply = self.callback_new_client()
            print("Replying to client: {}".format(reply))
            self.receiver.reply(cor_id, reply_to, reply)
            print("Replied successfully")
            self.state_saver.save_state("STATE", conn_id, json.dumps([conn_id, "BLOCKED"]))

    def restart_all_senders(self, conn_id):
        for sender in self.senders:
            sender.send(RESTART, conn_id)
