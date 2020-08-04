import json
import uuid

from protocol.protocol import Protocol
from collections import Counter
from secure_data.secure_data import SecureData

from duplicate_filter.duplicate_filter import DuplicateFilter

STAGE = "top_cities"
TOP_MSG_ID = "top_cities"
STATE_FILE = "top_cities_resume.txt"

class TopCitiesController:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(recv_queue, send_queue, total_workers, status_queue)
        self.cities_data = {}
        self.top_cities = {}
        self.duplicate_filter = DuplicateFilter(data_cluster_write, data_cluster_read)
        self.secure_data = SecureData(data_cluster_write, data_cluster_read)
        self.connection_id = None

    def start(self):
        self.protocol.start_connection(self.data_read, self.process_results)
        #self.process_results()

    def data_read(self, msg):
        [connection_id, message_id, data_str] = msg.split("@@")
        if self.duplicate_filter.message_exists(connection_id, STAGE, message_id):
            print("Duplicated message: " + message_id)
            return

        if connection_id != self.connection_id:
            old_data = self.secure_data.read_file(connection_id + "/" + STAGE, STATE_FILE)
            if old_data is not None and old_data != "":
                self.cities_data = json.loads(old_data)

        self.connection_id = connection_id
        data = json.loads(data_str)
        self.cities_data.update(data)

        self.secure_data.write_to_file(
            connection_id + "/" + STAGE,
            STATE_FILE,
            json.dumps(self.cities_data)
        )
        self.duplicate_filter.insert_message(connection_id, STAGE, message_id, ".")
    
    def process_results(self):
        self.top_cities = dict(Counter(self.cities_data).most_common(3))
        data = self.connection_id + "@@" + TOP_MSG_ID + "@@" + json.dumps(self.top_cities)

        self.protocol.send_data(data)
