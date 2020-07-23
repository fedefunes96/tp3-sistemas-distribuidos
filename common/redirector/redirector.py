from redirector.protocol.protocol import Protocol

from duplicate_filter.duplicate_filter import DuplicateFilter


class Redirector:
    def __init__(self, recv_queue, send_queues, master_send_queue, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(recv_queue, send_queues, master_send_queue, status_queue)
        self.duplicate_filter = DuplicateFilter(data_cluster_write, data_cluster_read)

    def start(self):
        self.protocol.start_connection(self.data_received, self.eof_received)

    def data_received(self, data):
        raise NotImplementedError

    def eof_received(self):
        pass

    def redirect_data(self, data, queue):
        self.protocol.send_data(data, queue)
