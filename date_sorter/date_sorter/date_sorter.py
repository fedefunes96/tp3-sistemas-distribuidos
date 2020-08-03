import json
import uuid

from protocol.protocol import Protocol
from collections import OrderedDict

from duplicate_filter.duplicate_filter import DuplicateFilter

DATE_MSG_ID = "date_sorter"

class DateSorter:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(recv_queue, send_queue, total_workers, status_queue)
        self.date_data = OrderedDict()
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
        self.date_data.update(sorted(data.items()))
        self.duplicate_filter.insert_message(connection_id, message_id, msg)
    
    def process_results(self):
        data = self.connection_id + "@@" + DATE_MSG_ID + "@@" + json.dumps(self.date_data)
        self.protocol.send_data(data)
