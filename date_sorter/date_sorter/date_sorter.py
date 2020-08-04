from protocol.protocol import Protocol
from collections import OrderedDict

class DateSorter:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(
            recv_queue,
            send_queue,
            total_workers,
            status_queue,
            data_cluster_write,
            data_cluster_read
        )

        self.date_data = OrderedDict()

    def start(self):
        self.protocol.start_connection(
            self.data_read,
            self.process_results,
            self.load_data,
            self.reset_data,
            self.save_data            
        )

    def data_read(self, data):
        self.date_data.update(sorted(data.items()))
    
    def process_results(self):
        self.protocol.send_data(self.date_data)

    def load_data(self, date_data):
        self.date_data = date_data

    def reset_data(self):
        self.date_data = OrderedDict()

    def save_data(self):
        return self.date_data
