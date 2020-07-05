from protocol.protocol import Protocol
from collections import Counter

class Worker:
    def __init__(self, recv_queue, send_queue):
        self.protocol = Protocol(recv_queue, send_queue)
        self.total_positivi = 0
        self.total_deceduti = 0

    def start(self):
        self.protocol.start_connection(self.data_read)

        self.process_results()

    def data_read(self, positivi, deceduti):
        self.total_positivi += positivi
        self.total_deceduti += deceduti
    
    def process_results(self):
        result = self.total_deceduti / self.total_positivi

        self.protocol.send_data(result)
