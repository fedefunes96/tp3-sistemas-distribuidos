from middleware.connection import Connection
from communication.message_types import READY, NEW_CLIENT, RESTART
from middleware.secure_connection.secure_rpc_receiver import SecureRpcReceiver
from middleware.secure_connection.secure_direct_sender import SecureDirectSender
from middleware.secure_connection.secure_rpc_sender import SecureRpcSender

import json

class Protocol:
    def __init__(self, recv_queue, send_queues, state_saver, place_manager_queue):
        self.connection = Connection()
                  
        self.receiver = SecureRpcReceiver(recv_queue, self.connection)

        self.senders = []
        self.state_saver = state_saver

        for queue in send_queues:
            self.senders.append(SecureDirectSender(queue, self.connection))
        
        self.place_manager_sender = SecureRpcSender(place_manager_queue, Connection())

    def start_receiving(self, callback_restart, callback_new_client):
        self.callback_restart = callback_restart
        self.callback_new_client = callback_new_client

        self.receiver.start_receiving(self.data_read)

    def data_read(self, reply_to, cor_id, msg):
        [conn_id, msg_type] = json.loads(msg)
        print("Received {}".format(msg))

        duplicate_message_id = conn_id + "-" + msg_type
        if self.state_saver.is_duplicated("STATE", duplicate_message_id):
            print("Duplicated message: {}".format(duplicate_message_id))
            return

        if msg_type == RESTART:
            self.state_saver.save_state("STATE", duplicate_message_id, json.dumps([conn_id, "RESTART"]))
            self.callback_restart(conn_id)
            self.receiver.reply(cor_id, reply_to, READY)
            self.state_saver.save_state("STATE", duplicate_message_id, json.dumps([conn_id, "READY"]))
        elif msg_type == NEW_CLIENT:
            reply = self.callback_new_client(conn_id)
            print("Replying to client: {}".format(reply))
            print("Replying to queue: {}".format(reply_to))
            self.receiver.reply(cor_id, reply_to, reply)
            print("Replied successfully")
            self.state_saver.save_state("STATE", duplicate_message_id, json.dumps([conn_id, "BLOCKED"]))

    def restart_all_senders(self, conn_id):
        self.place_manager_sender.send(json.dumps([RESTART, conn_id]))

        for sender in self.senders:
            sender.send(RESTART, conn_id)