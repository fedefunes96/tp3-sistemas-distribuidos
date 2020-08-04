import uuid
import json

from protocol.protocol import Protocol

from secure_data.secure_data import SecureData

class Worker:
    def __init__(self, recv_queue, send_queue, master_queue, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(
            recv_queue,
            send_queue,
            master_queue,
            status_queue,
            data_cluster_write,
            data_cluster_read
        )
        self.positives_per_city = {}

    def start(self):
        self.protocol.start_connection(
            self.data_read,
            self.process_results,
            self.load_data,
            self.reset_data,
            self.save_data
        )

    def data_read(self, place):
        if place not in self.positives_per_city:
            self.positives_per_city[place] = 0
            
        self.positives_per_city[place] += 1
        print("Positive of {}".format(place))

    def load_data(self, positives_per_city):
        self.positives_per_city = positives_per_city

    def reset_data(self):
        self.positives_per_city = {}

    def save_data(self):
        return self.positives_per_city

    def process_results(self):
        self.protocol.send_data(self.positives_per_city)
