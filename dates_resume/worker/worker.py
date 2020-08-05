from protocol.protocol import Protocol

class Worker:
    def __init__(self, recv_queue, send_queue, status_queue, data_cluster_write, data_cluster_read):
        self.protocol = Protocol(
            recv_queue,
            send_queue,
            status_queue,
            data_cluster_write,
            data_cluster_read
        )

        self.results_per_date = {}

    def start(self):
        self.protocol.start_connection(
            self.data_read,
            self.process_results,
            self.load_data,
            self.reset_data,
            self.save_data            
        )

    def data_read(self, date, result):
        if date not in self.results_per_date:
            self.results_per_date[date] = [0, 0]
        
        if result == "positivi":
            self.results_per_date[date][0] += 1
        else:
            self.results_per_date[date][1] += 1

    def process_results(self):
        self.protocol.send_data(self.results_per_date)

    def load_data(self, date_results):
        self.results_per_date = date_results

    def reset_data(self):
        self.results_per_date = {}

    def save_data(self):
        return self.results_per_date
