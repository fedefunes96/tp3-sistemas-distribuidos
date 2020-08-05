import csv
from count_redirector.count_redirector import CountRedirector

class Worker:
    def __init__(self,
        recv_queue,
        send_queue,
        master_queue,
        status_queue,
        data_cluster_write,
        data_cluster_read,
        worker_id
    ):
        self.redirector = CountRedirector(
            recv_queue,
            send_queue,
            master_queue,
            self.data_received,
            self.no_more_data,
            status_queue,
            data_cluster_write,
            data_cluster_read,
            worker_id,
            self.load_data,
            self.reset_data,
            self.save_data
        )

        self.total_deceduti = 0
        self.total_positivi = 0

    def start(self):
        self.redirector.start()
    
    def no_more_data(self):
        self.redirector.send_data(self.total_positivi, self.total_deceduti)

    def data_received(self, result):
        if result == "positivi":
            self.total_positivi += 1
        else:
            self.total_deceduti += 1

    def load_data(self, data):
        self.total_positivi = data[0]
        self.total_deceduti = data[1]

    def reset_data(self):
        self.total_deceduti = 0
        self.total_positivi = 0

    def save_data(self):
        return [self.total_positivi, self.total_deceduti]
