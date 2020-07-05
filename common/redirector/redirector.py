from redirector.protocol.protocol import Protocol

class Redirector:
    def __init__(self, recv_queue, send_queues, master_send_queue):
        self.protocol = Protocol(recv_queue, send_queues, master_send_queue)

    def start(self):
        self.protocol.start_connection(self.data_received, self.eof_received)

    def data_received(self, data):
        raise NotImplementedError

    def eof_received(self):
        pass

    def redirect_data(self, data, queue):
        self.protocol.send_data(data, queue)
