import json
import uuid

from protocol.protocol import Protocol

from duplicate_filter.duplicate_filter import DuplicateFilter
from secure_data.secure_data import SecureData

REDUCER_NAME = "dates_resume"

class Worker:
    def __init__(self, recv_queue, send_queue, master_queue, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(
            recv_queue,
            send_queue,
            master_queue,
            status_queue
        )
        self.duplicate_filter = DuplicateFilter(data_cluster_write, data_cluster_read)
        self.secure_data = SecureData(data_cluster_write, data_cluster_read)
        self.connection_id = ""
        self.results_per_date = {}

    def start(self):
        self.protocol.start_connection(self.data_read, self.process_results)

        #self.process_results()

    def data_read(self, msg):
        [connection_id, message_id, date, result] = msg.split(',')
        if self.duplicate_filter.message_exists(connection_id, message_id):
            print("Duplicated message: " + message_id)
            return
        if connection_id != self.connection_id:
            self.results_per_date = json.loads(self.secure_data.read_file(connection_id, REDUCER_NAME))

        self.connection_id = connection_id
        if date not in self.results_per_date:
            self.results_per_date[date] = [0, 0]
        
        if result == "positivi":
            self.results_per_date[date][0] += 1
        else:
            self.results_per_date[date][1] += 1

        self.secure_data.write_to_file(connection_id, REDUCER_NAME, json.dumps(self.results_per_date))
        self.duplicate_filter.insert_message(connection_id, message_id, msg)

    def process_results(self):
        msg = self.connection_id + "@@" + str(uuid.uuid4()) + "@@" + json.dumps(self.results_per_date)
        self.protocol.send_data(msg)
