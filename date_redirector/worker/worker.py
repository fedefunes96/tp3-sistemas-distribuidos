import csv
from date_redirector.date_redirector import DateRedirector
from state_saver.state_saver import StateSaver
import json
from coordinator.coordinator import Coordinator
from secure_data.secure_data import SecureData

GLOBAL_STAGE = "date_redirector"

class Worker:
    def __init__(self, recv_queue, send_queue, master_queue, status_queue, data_cluster_write, data_cluster_read, my_id):
        self.my_id = my_id
        self.global_saver = StateSaver(GLOBAL_STAGE, data_cluster_write, data_cluster_read)
        self.single_saver = StateSaver(my_id, data_cluster_write, data_cluster_read)

        self.date_redirector = DateRedirector(
            recv_queue,
            send_queue,
            master_queue,
            status_queue,
            self.global_saver,
            self.single_saver,
            self.my_id
        )

        self.coordinator = Coordinator(
            self.my_id,
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
            self.date_redirector.start()
