from redirector.redirector import Redirector

class DateRedirector(Redirector):
    def __init__(self, recv_queue, send_queues, master_send_queue):
        self.send_queues = send_queues
        Redirector.__init__(self, recv_queue, send_queues, master_send_queue)

    def data_received(self, data):
        [date, latitude, longitude, result] = data.split(",")

        new_data = date + ',' + result

        self.redirect_data(new_data, self.send_queues[0])
