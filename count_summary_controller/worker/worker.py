from protocol.protocol import Protocol
from collections import Counter

from duplicate_filter.duplicate_filter import DuplicateFilter
from secure_data.secure_data import SecureData

STATE_POSITIVES_FILE = "count_resume_positives.txt"
STATE_DEATHS_FILE = "count_resume_deaths.txt"
COUNT_MSG_ID = "count_resumer"
STAGE = "count_resume"

class Worker:
    def __init__(self, recv_queue, send_queue, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(recv_queue, send_queue, status_queue)
        self.total_positivi = 0
        self.total_deceduti = 0
        self.duplicate_filter = DuplicateFilter(data_cluster_write, data_cluster_read)
        self.secure_data = SecureData(data_cluster_write, data_cluster_read)
        self.connection_id = ""

    def start(self):
        self.protocol.start_connection(self.data_read, self.process_results)

    def data_read(self, msg):
        [connection_id, message_id, positivi, deceduti] = msg.split(',')
        if self.duplicate_filter.message_exists(connection_id, STAGE, message_id):
            print("Duplicated message: " + message_id)
            return
        if connection_id != self.connection_id:
            old_positive_data = self.secure_data.read_file(connection_id + "/" + STAGE, STATE_POSITIVES_FILE)
            if old_positive_data is not None and old_positive_data != "":
                self.total_positivi = int(old_positive_data)
            old_death_data = self.secure_data.read_file(connection_id + "/" + STAGE, STATE_DEATHS_FILE)
            if old_death_data is not None and old_death_data != "":
                self.total_deceduti = int(old_death_data)

        self.connection_id = connection_id

        self.total_positivi += int(positivi)
        self.total_deceduti += int(deceduti)

        self.secure_data.write_to_file(connection_id + "/" + STAGE, STATE_POSITIVES_FILE, str(self.total_positivi))
        self.secure_data.write_to_file(connection_id + "/" + STAGE, STATE_DEATHS_FILE, str(self.total_deceduti))
        self.duplicate_filter.insert_message(connection_id, STAGE, message_id, ".")

    def process_results(self):
        result = self.total_deceduti / self.total_positivi

        msg = self.connection_id + "@@" + COUNT_MSG_ID + "@@" + str(result)

        self.protocol.send_data(msg)
