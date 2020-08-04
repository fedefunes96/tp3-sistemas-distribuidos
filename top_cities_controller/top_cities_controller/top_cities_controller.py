from protocol.protocol import Protocol
from collections import Counter

class TopCitiesController:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(
            recv_queue,
            send_queue,
            total_workers,
            status_queue,
            data_cluster_write,
            data_cluster_read
        )

        self.cities_data = {}

    def start(self):
        self.protocol.start_connection(
            self.data_read,
            self.process_results,
            self.load_data,
            self.reset_data,
            self.save_data                
        )

    def data_read(self, cities_data):
        self.cities_data.update(cities_data)
    
    def process_results(self):
        top_cities = dict(Counter(self.cities_data).most_common(3))

        self.protocol.send_data(top_cities)

    def load_data(self, cities_data):
        self.cities_data = cities_data

    def reset_data(self):
        self.cities_data = {}

    def save_data(self):
        return self.cities_data
