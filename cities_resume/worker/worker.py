import uuid
import json

from protocol.protocol import Protocol

from duplicate_filter.duplicate_filter import DuplicateFilter

from secure_data.secure_data import SecureData

REDUCER_NAME = "cities_resume"
STAGE = "cities_resume"
PLACE_MSG_ID = "cities_resume_a_places"

class Worker:
    def __init__(self, recv_queue, send_queue, master_queue, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(
            recv_queue,
            send_queue,
            master_queue,
            status_queue
        )
        self.positives_per_city = {}
        self.duplicate_filter = DuplicateFilter(data_cluster_write, data_cluster_read)
        self.secure_data = SecureData(data_cluster_write, data_cluster_read)
        self.connection_id = None

    def start(self):
        self.protocol.start_connection(self.data_read, self.process_results)

    def data_read(self, msg):
        [connection_id, message_id, place] = msg.split(",")

        if self.duplicate_filter.message_exists(connection_id, STAGE, message_id):
            print("Duplicated message: " + message_id)
            return
        if connection_id != self.connection_id:
            old_data = self.secure_data.read_file(connection_id, REDUCER_NAME)
            if old_data is not None and old_data != "":
                self.positives_per_city = json.loads(old_data)
        self.connection_id = connection_id

        if place not in self.positives_per_city:
            self.positives_per_city[place] = 0
            
        self.positives_per_city[place] += 1
        print("Positive of {}".format(place))

        self.secure_data.write_to_file(connection_id, REDUCER_NAME, json.dumps(self.positives_per_city))
        self.duplicate_filter.insert_message(connection_id, STAGE, message_id, ".")

    def process_results(self):
        #Unique message so that if this fails, the next one that raises will
        #send the same id
        data = self.connection_id + "@@" + PLACE_MSG_ID + "@@" + json.dumps(self.positives_per_city)
        self.protocol.send_data(data)
