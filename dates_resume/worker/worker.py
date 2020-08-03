import json
import uuid

from protocol.protocol import Protocol

from duplicate_filter.duplicate_filter import DuplicateFilter

DATE_MSG_ID = "dates_resume_jan"
STAGE = "date_resume"

class Worker:
    def __init__(self, recv_queue, send_queue, master_queue, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(
            recv_queue,
            send_queue,
            master_queue,
            status_queue
        )
        self.duplicate_filter = DuplicateFilter(data_cluster_write, data_cluster_read)
        self.connection_id = ""
        self.results_per_date = {}

    def start(self):
        self.protocol.start_connection(self.data_read, self.process_results)

        #self.process_results()

    def data_read(self, msg):
        [connection_id, message_id, date, result] = msg.split(',')
        if self.duplicate_filter.message_exists(connection_id, STAGE, message_id):
            print("Duplicated message: " + message_id)
            return
        self.connection_id = connection_id
        if date not in self.results_per_date:
            self.results_per_date[date] = [0, 0]
        
        if result == "positivi":
            self.results_per_date[date][0] += 1
        else:
            self.results_per_date[date][1] += 1

        self.duplicate_filter.insert_message(connection_id, STAGE, message_id, ".")
    
    def process_results(self):
        msg = self.connection_id + "@@" + DATE_MSG_ID + "@@" + json.dumps(self.results_per_date)
        self.protocol.send_data(msg)
