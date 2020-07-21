from middleware.connection import Connection

class Protocol:
    def __init__(self, recv_queue):
        #Temp solution
        conn = False

        while conn == False:
            try:
                self.connection = Connection()
                conn = True
            except:
                pass

        self.receiver = self.connection.create_direct_receiver(recv_queue)
    
    def start_receiving(self, callback):
        self.callback = callback
        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        [status, worker_id, worker_type] = msg.split(',')

        self.callback(status, worker_id, worker_type)
