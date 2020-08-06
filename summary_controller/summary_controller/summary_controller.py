from protocol.protocol import Protocol
import json

FOLDER_WRITE = 'summary/'
STAGE = "summary"
DIRECTORY_NAME = "resume_data"
CITIES_TOTAL_NAME = "cities_total_name.txt"
DATES_TOTAL_NAME = "dates_total_name.txt"
COUNT_TOTAL_NAME = "count_total_name.txt"

class SummaryController:
    def __init__(self,
        recv_queue,
        status_queue,
        data_cluster_write,
        data_cluster_read,
        coordinator_queue
    ):
        self.protocol = Protocol(
            recv_queue,
            status_queue,
            data_cluster_write,
            data_cluster_read,
            coordinator_queue
        )

        self.top_cities = None
        self.date_data = None
        self.percentage = None

    def start(self):
        self.protocol.start_connection(
            self.top_cities_read,
            self.date_data_read,
            self.count_read,
            self.write_summary,
            self.load_data,
            self.reset_data,
            self.save_data
        )

    def top_cities_read(self, top_cities):
        self.top_cities = top_cities

    def date_data_read(self, date_data):
        self.date_data = date_data

    def count_read(self, percentage):
        if percentage.isdigit():
            self.percentage = float(percentage) * 100
        else:
            self.percentage = percentage

    def write_summary(self, conn_id):
        print("Starting to write file {}".format(FOLDER_WRITE + 'summary_' + conn_id + '.txt'))
        with open(FOLDER_WRITE + 'summary_' + conn_id + '.txt', 'w') as file:
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

    def load_data(self, data):
        self.top_cities = data[0]
        self.date_data = data[1]
        self.percentage = data[2]

    def reset_data(self):
        self.top_cities = None
        self.date_data = None
        self.percentage = None

    def save_data(self):
        return [self.top_cities, self.date_data, self.percentage]
