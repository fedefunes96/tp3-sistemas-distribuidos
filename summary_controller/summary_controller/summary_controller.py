from protocol.protocol import Protocol
import json

from duplicate_filter.duplicate_filter import DuplicateFilter
from secure_data.secure_data import SecureData

FOLDER_WRITE = 'summary/'
STAGE = "summary"
DIRECTORY_NAME = "resume_data"
CITIES_TOTAL_NAME = "cities_total_name.txt"
DATES_TOTAL_NAME = "dates_total_name.txt"
COUNT_TOTAL_NAME = "count_total_name.txt"


class SummaryController:
    def __init__(self, recv_queue, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(recv_queue, status_queue)
        self.duplicate_filter = DuplicateFilter(data_cluster_write, data_cluster_read)
        self.secure_data = SecureData(data_cluster_write, data_cluster_read)
        self.conn_id = None

    def start(self):
        self.protocol.start_connection(
            self.top_cities_read,
            self.date_data_read,
            self.count_read,
            self.write_summary
        )

    def top_cities_read(self, msg):
        [connection_id, message_id, top_cities_str] = msg.split("@@")

        if self.conn_id != connection_id:
            self.conn_id = connection_id
            self.read_all_files()

        if self.duplicate_filter.message_exists(connection_id, STAGE, message_id):
            print("Duplicated message: " + message_id)
            return

        print("Received: {}".format(top_cities_str))
        self.top_cities = json.loads(top_cities_str)

        self.secure_data.write_to_file(self.conn_id + "/" + DIRECTORY_NAME, CITIES_TOTAL_NAME, json.dumps(self.top_cities))
        self.duplicate_filter.insert_message(connection_id, STAGE, message_id, ".")

    def date_data_read(self, msg):
        [connection_id, message_id, date_data_str] = msg.split("@@")

        if self.conn_id != connection_id:
            self.conn_id = connection_id
            self.read_all_files()

        if self.duplicate_filter.message_exists(connection_id, STAGE, message_id):
            print("Duplicated message: " + message_id)
            return

        self.date_data = json.loads(date_data_str)

        self.secure_data.write_to_file(self.conn_id + "/" + DIRECTORY_NAME, DATES_TOTAL_NAME, json.dumps(self.date_data))
        self.duplicate_filter.insert_message(connection_id, STAGE, message_id, ".")

    def count_read(self, msg):
        [connection_id, message_id, percentage] = msg.split("@@")

        if self.conn_id != connection_id:
            self.conn_id = connection_id
            self.read_all_files()

        if self.duplicate_filter.message_exists(connection_id, STAGE, message_id):
            print("Duplicated message: " + message_id)
            return

        self.percentage = float(percentage) * 100

        self.secure_data.write_to_file(self.conn_id + "/" + DIRECTORY_NAME, COUNT_TOTAL_NAME, str(self.percentage))
        self.duplicate_filter.insert_message(connection_id, STAGE, message_id, ".")

    def write_summary(self):
        print("Starting to write file {}".format(FOLDER_WRITE + 'summary_' + self.conn_id + '.txt'))
        with open(FOLDER_WRITE + 'summary_' + self.conn_id + '.txt', 'w') as file:
            file.write("date - totale_positivi - totale_deceduti\n")
            for date in self.date_data:
                file.write(
                    date +
                    " - " +
                    str(self.date_data[date][0]) +
                    " - " +
                    str(self.date_data[date][1]) +
                    "\n"
                )

            file.write("\nTop 3 cities - totale positivi\n")
            for place in self.top_cities:
                file.write(
                    place +
                    " - " +
                    str(self.top_cities[place]) +
                    "\n"
                )

            file.write("\nPorcentuale Deceduti=")
            file.write(str(self.percentage) + "%")
        #self.secure_data.write_to_file(self.conn_id + "/" + DIRECTORY_NAME, CITIES_TOTAL_NAME, "")
        #self.secure_data.write_to_file(self.conn_id + "/" + DIRECTORY_NAME, COUNT_TOTAL_NAME, "")
        #self.secure_data.write_to_file(self.conn_id + "/" + DIRECTORY_NAME, DATES_TOTAL_NAME, "")

    def read_all_files(self):
        self.read_cities_file()
        self.read_dates_file()
        self.read_total_file()

    def read_cities_file(self):
        data = self.secure_data.read_file(self.conn_id + "/" + DIRECTORY_NAME, CITIES_TOTAL_NAME)
        if data is not None and data != "":
            self.top_cities = json.loads(data)
            self.protocol.add_already_read()

    def read_dates_file(self):
        data = self.secure_data.read_file(self.conn_id + "/" + DIRECTORY_NAME, DATES_TOTAL_NAME)
        if data is not None and data != "":
            self.date_data = json.loads(data)
            self.protocol.add_already_read()

    def read_total_file(self):
        data = self.secure_data.read_file(self.conn_id + "/" + DIRECTORY_NAME, COUNT_TOTAL_NAME)
        if data is not None and data != "":
            self.percentage = float(data)
            self.protocol.add_already_read()
