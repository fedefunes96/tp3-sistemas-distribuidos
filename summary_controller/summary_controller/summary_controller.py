from protocol.protocol import Protocol
import json

WRITE_FILE = 'summary/summary.txt'

class SummaryController:
    def __init__(self, recv_queue):
        self.protocol = Protocol(recv_queue)

    def start(self):
        self.protocol.start_connection(
            self.top_cities_read,
            self.date_data_read,
            self.count_read
        )

        self.write_summary()

    def top_cities_read(self, top_cities):
        self.top_cities = top_cities

    def date_data_read(self, date_data):
        self.date_data = date_data

    def count_read(self, percentage):
        self.percentage = percentage * 100
    
    def write_summary(self):
        print("Starting to write file")
        with open(WRITE_FILE, 'w') as file:
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
