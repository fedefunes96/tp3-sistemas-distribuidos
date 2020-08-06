import csv
from count_redirector.count_redirector import CountRedirector
from state_saver.state_saver import StateSaver
from secure_data.secure_data import SecureData

import json
from coordinator.coordinator import Coordinator

GLOBAL_STAGE = "count_worker"

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
        self.global_saver = StateSaver(GLOBAL_STAGE, data_cluster_write, data_cluster_read)
        self.single_saver = StateSaver(worker_id, data_cluster_write, data_cluster_read)

        self.redirector = CountRedirector(
            recv_queue,
            send_queue,
            master_queue,
            self.data_received,
            self.no_more_data,
            status_queue,
            self.global_saver,
            self.single_saver,
            worker_id,
            self.load_data,
            self.reset_data,
            self.save_data
        )

        self.total_deceduti = 0
        self.total_positivi = 0

        self.coordinator = Coordinator(
            worker_id,
            data_cluster_write,
            data_cluster_read
        )

    def start(self):
        state = self.single_saver.load_state("STATE")
                    
        if state == "WAITING":
            #Wait for coordinator
            print("Waiting for coordinator")
            self.coordinator.wait_to_work()
            self.single_saver.save_state("STATE", "", "READY")
        else:
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
