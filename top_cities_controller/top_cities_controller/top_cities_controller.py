from protocol.protocol import Protocol
from collections import Counter

class TopCitiesController:
    def __init__(self, recv_queue, send_queue, total_workers):
        self.protocol = Protocol(recv_queue, send_queue, total_workers)
        self.cities_data = {}
        self.top_cities = {}

    def start(self):
        self.protocol.start_connection(self.data_read)
        self.process_results()

    def data_read(self, data):
        self.cities_data.update(data)
    
    def process_results(self):
        self.top_cities = dict(Counter(self.cities_data).most_common(3))

        self.protocol.send_data(self.top_cities)
