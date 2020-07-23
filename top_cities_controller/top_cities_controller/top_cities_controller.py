import json
import uuid

from protocol.protocol import Protocol
from collections import Counter

from common.duplicate_filter.duplicate_filter import DuplicateFilter


class TopCitiesController:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(recv_queue, send_queue, total_workers, status_queue)
        self.cities_data = {}
        self.top_cities = {}
        self.duplicate_filter = DuplicateFilter(data_cluster_write, data_cluster_read)
        self.connection_id = ""

    def start(self):
        self.protocol.start_connection(self.data_read, self.process_results)
        #self.process_results()

    def data_read(self, msg):
        [connection_id, message_id, data_str] = msg.split("@@")
        if self.duplicate_filter.message_exists(connection_id, message_id):
            print("Duplicated message: " + message_id)
            return
        self.connection_id = connection_id
        data = json.loads(data_str)
        self.cities_data.update(data)
        self.duplicate_filter.insert_message(connection_id, message_id, msg)
    
    def process_results(self):
        self.top_cities = dict(Counter(self.cities_data).most_common(3))
        data = self.connection_id + "@@" + str(uuid.uuid4()) + json.dumps(self.top_cities)

        self.protocol.send_data(data)
