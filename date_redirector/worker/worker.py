import csv
from date_redirector.date_redirector import DateRedirector

class Worker:
    def __init__(self, recv_queue, send_queue, master_queue):
        self.date_redirector = DateRedirector(
            recv_queue,
            send_queue,
            master_queue
        )

    def start(self):
        self.date_redirector.start()
