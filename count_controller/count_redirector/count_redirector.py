from redirector.redirector import Redirector

class CountRedirector(Redirector):
    def __init__(self, recv_queue, send_queue, master_send_queue, callback, callback_eof):
        self.send_queue = send_queue
        self.callback = callback
        self.callback_eof = callback_eof

        Redirector.__init__(self, recv_queue, [send_queue], master_send_queue)

    def data_received(self, data):
        [date, latitude, longitude, result] = data.split(",")
        self.callback(result)

    def eof_received(self):
        self.callback_eof()

    def send_data(self, positives, deceased):
        msg = str(positives) + "," + str(deceased)
        self.redirect_data(msg, self.send_queue)
