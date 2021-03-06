from redirector.protocol.protocol import Protocol

class Redirector:
    def __init__(self, recv_queue, send_queues, master_send_queue, status_queue, state_saver, my_id):
        self.protocol = Protocol(recv_queue, send_queues, master_send_queue, status_queue, state_saver, my_id)

    def start(self):
        self.protocol.start_connection(self.data_received, self.eof_received)

    def data_received(self, data):
        raise NotImplementedError

    def eof_received(self, msg):
        pass

    def redirect_data(self, data, queue):
        self.protocol.send_data(data, queue)
