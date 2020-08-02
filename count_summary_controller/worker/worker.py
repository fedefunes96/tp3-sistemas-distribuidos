import uuid

from protocol.protocol import Protocol
from collections import Counter

from duplicate_filter.duplicate_filter import DuplicateFilter

COUNT_MSG_ID = "count_resumer"

class Worker:
    def __init__(self, recv_queue, send_queue, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(recv_queue, send_queue, status_queue)
        self.total_positivi = 0
        self.total_deceduti = 0
        self.duplicate_filter = DuplicateFilter(data_cluster_write, data_cluster_read)
        self.connection_id = ""

    def start(self):
        self.protocol.start_connection(self.data_read, self.process_results)

    def data_read(self, msg):
        [connection_id, message_id, positivi, deceduti] = msg.split(',')
        if self.duplicate_filter.message_exists(connection_id, message_id):
            print("Duplicated message: " + message_id)
            return
        self.connection_id = connection_id

        self.total_positivi += int(positivi)
        self.total_deceduti += int(deceduti)

        self.duplicate_filter.insert_message(connection_id, message_id, msg)

    def process_results(self):
        result = self.total_deceduti / self.total_positivi

        msg = self.connection_id + "@@" + COUNT_MSG_ID + "@@" + str(result)

        self.protocol.send_data(msg)
