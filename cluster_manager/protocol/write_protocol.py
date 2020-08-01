from middleware.connection import Connection
from communication.message_types import WRITE_OK, FAILED, APPEND, WRITE
import os
from middleware.secure_connection.secure_rpc_receiver import SecureRpcReceiver
from middleware.secure_connection.secure_rpc_sender import SecureRpcSender

class WriteProtocol:
    def __init__(self, recv_queue, send_queues):
        self.connection = Connection()

        self.receiver = SecureRpcReceiver(recv_queue, self.connection)
        self.senders = []

        for queue in send_queues:
            print("Linking senders to: {}".format(queue))
            #self.senders.append(self.connection.create_rpc_sender(queue))
            self.senders.append(SecureRpcSender(queue, self.connection))

    def start_receiving(self, callback_app, callback_wr):
        self.callback_app = callback_app
        self.callback_wr = callback_wr

        print("Starting to receive Write calls")
        self.receiver.start_receiving(self.data_read)
    
    def replicate_data(self, folder_to_write, file_to_write, data, mode):
        pending_ack = len(self.senders)
        msg = folder_to_write + "@@" + file_to_write + "@@" + data + "@@" + mode
        
        for sender in self.senders:
            print("Sending replica to: {}".format(sender))
            try:
                answer = sender.send(msg)

                print("Received answer: {}".format(answer))

                if answer == WRITE_OK:
                    pending_ack -= 1
                
                print("Received replica from {}".format(sender))
            except:
                pending_ack -= 1
                print("Exception in replica")
        
        print("Data replicated")

        if pending_ack == 0:
            return WRITE_OK
        
        return FAILED

    def data_read(self, reply_to, cor_id, msg):
        print("Received {}".format(msg))
        [folder_to_read, file_to_read, data, operation] = msg.split('@@')

        if operation == APPEND:
            reply = self.callback_app(folder_to_read, file_to_read, data)
            self.receiver.reply(cor_id, reply_to, reply)
        elif operation == WRITE:
            reply = self.callback_wr(folder_to_read, file_to_read, data)
            self.receiver.reply(cor_id, reply_to, reply)
