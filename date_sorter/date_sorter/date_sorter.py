import json
import uuid

from protocol.protocol import Protocol
from collections import OrderedDict
from secure_data.secure_data import SecureData

from duplicate_filter.duplicate_filter import DuplicateFilter

DATE_MSG_ID = "date_sorter"
STAGE = "date_sorter"
STATE_FILE = "date_sorter_resume.txt"

class DateSorter:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(recv_queue, send_queue, total_workers, status_queue)
        self.date_data = OrderedDict()
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
                self.date_data = json.loads(old_data)

        self.connection_id = connection_id
        data = json.loads(data_str)
        self.date_data.update(sorted(data.items()))

        self.secure_data.write_to_file(
            connection_id + "/" + STAGE,
            STATE_FILE,
            json.dumps(self.date_data)
        )        
        self.duplicate_filter.insert_message(connection_id, STAGE, message_id, ".")
    
    def process_results(self):
        data = self.connection_id + "@@" + DATE_MSG_ID + "@@" + json.dumps(self.date_data)
        self.protocol.send_data(data)
