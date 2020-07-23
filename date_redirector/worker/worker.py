import csv
from date_redirector.date_redirector import DateRedirector

class Worker:
    def __init__(self, recv_queue, send_queue, master_queue, status_queue, data_cluster_write, data_cluster_read):
        self.date_redirector = DateRedirector(
            recv_queue,
            send_queue,
            master_queue,
            status_queue,
            data_cluster_write,
            data_cluster_read
        )

    def start(self):
        self.date_redirector.start()
