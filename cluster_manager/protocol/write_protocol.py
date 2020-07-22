from middleware.connection import Connection
from communication.message_types import REPLICA, WRITE_OK, FAILED, APPEND, WRITE

class WriteProtocol:
    def __init__(self, recv_queue, send_queues):
        self.connection = Connection()
        self.receiver = self.connection.create_rpc_receiver(recv_queue)
        self.senders = []

        for queue in send_queues:
            self.senders.append(self.connection.create_rpc_sender(queue))

    def start_receiving(self, callback_app, callback_wr):
        self.callback_app = callback_app
        self.callback_wr = callback_wr

        self.receiver.start_receiving(self.data_read)
    
    def replicate_data(self, folder_to_write, file_to_write, data, mode):
        pending_ack = len(self.senders)
        msg = folder_to_write + "@@" + file_to_write + "@@" + data + "@@" + mode
        
        for sender in self.senders:
            try:
                answer = sender.send(msg)

                if answer == WRITE_OK:
                    pending_ack -= 1
            except:
                pending_ack -= 1
        
        if pending_ack == 0:
            return WRITE_OK
        
        return FAILED

    def data_read(self, reply_to, cor_id, msg):
        [folder_to_read, file_to_read, data, operation] = msg.split('@@')

        if operation == APPEND:
            reply = self.callback_app(folder_to_read, file_to_read, data)
            self.receiver.reply(cor_id, reply_to, reply)
        elif operation == WRITE:
            reply = self.callback_wr(folder_to_read, file_to_read, data)
            self.receiver.reply(cor_id, reply_to, reply)
