from protocol.protocol import Protocol
from collections import Counter

STATE_POSITIVES_FILE = "count_resume_positives.txt"
STATE_DEATHS_FILE = "count_resume_deaths.txt"
COUNT_MSG_ID = "count_resumer"
STAGE = "count_resume"

class Worker:
    def __init__(self, recv_queue, send_queue, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(
            recv_queue,
            send_queue,
            status_queue,
            data_cluster_write,
            data_cluster_read
        )

        self.total_positivi = 0
        self.total_deceduti = 0

    def start(self):
        self.protocol.start_connection(
            self.data_read,
            self.process_results,
            self.load_data,
            self.reset_data,
            self.save_data            
        )

    def data_read(self, positivi, deceduti):
        self.total_positivi += int(positivi)
        self.total_deceduti += int(deceduti)

    def process_results(self):
        result = "Not possible"

        if self.total_positivi != 0:
            result = str(self.total_deceduti / self.total_positivi)

        self.protocol.send_data(result)

    def load_data(self, data):
        self.total_positivi = data[0]
        self.total_deceduti = data[1]

    def reset_data(self):
        self.total_positivi = 0
        self.total_deceduti = 0

    def save_data(self):
        return [self.total_positivi, self.total_deceduti]