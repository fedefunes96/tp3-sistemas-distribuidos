from middleware.connection import Connection

from communication.message_types import EOF


class Protocol:
    def __init__(self, recv_queue, send_queue, total_workers):
        self.connection = Connection()

        self.total_workers = total_workers

        self.receiver = self.connection.create_direct_receiver(recv_queue)
        self.sender = self.connection.create_distributed_work_sender(send_queue)

    def start_connection(self):#, callback):
        #self.callback = callback

        self.receiver.start_receiving(self.data_read)
    
    #def send_data(self, data):
    #    self.sender.send(NORMAL, data)

    def data_read(self, msg_type, msg):
        self.receiver.close()
        self.send_eof()
        self.connection.close()        
        '''if msg_type == "EOF":
            self.receiver.close()
            self.send_eof()
            self.connection.close()
        else:            
            self.callback(msg)'''
        
    def send_eof(self):
        for i in range(0, self.total_workers):
            self.sender.send(EOF, '')
