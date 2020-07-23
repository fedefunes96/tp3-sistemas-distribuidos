from middleware.connection import Connection

class ReadProtocol:
    def __init__(self, recv_queue):
        #Temp solution
        conn = False

        while conn == False:
            try:
                self.connection = Connection()
                conn = True
            except:
                pass   
            
        self.receiver = self.connection.create_rpc_receiver(recv_queue)

    def start_receiving(self, callback):
        self.callback = callback

        self.receiver.start_receiving(self.data_read)

    def data_read(self, reply_to, cor_id, msg):
        [folder_to_read, file_to_read] = msg.split('@@')

        reply = self.callback(folder_to_read, file_to_read)

        self.receiver.reply(cor_id, reply_to, reply)
