from protocol.protocol import Protocol

class MasterController:
    def __init__(self, recv_queue, send_queue, total_workers):
        self.protocol = Protocol(recv_queue, send_queue, total_workers)

    def start(self):
        #self.protocol.start_connection(self.data_read)
        self.protocol.start_connection()

    #def data_read(self, data):
    #   self.protocol.send_data(data)
