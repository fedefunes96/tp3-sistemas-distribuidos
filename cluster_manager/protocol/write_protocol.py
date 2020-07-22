from middleware.connection import Connection

class WriteProtocol:
    def __init__(self, recv_queue, send_queues):
        self.connection = Connection()
        self.receiver = self.connection.create_rpc_receiver(recv_queue)
        self.senders = {}

        for queue in send_queues:
            self.senders[queue] = self.connection.create_rpc_sender(queue)

    def start_receiving(self, callback):
        self.callback = callback

        self.receiver.start_receiving(self.data_read)
    
    def send_data(self, data, where):
        self.senders[where].send(NORMAL, data)

    def data_read(self, reply_to, cor_id, msg):
        [folder_to_read, file_to_read, data] = msg.split(',')

        reply = self.callback(folder_to_read, file_to_read, data)

        self.receiver.reply(cor_id, reply_to, reply)
