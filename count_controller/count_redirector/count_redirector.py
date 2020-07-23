import uuid

from redirector.redirector import Redirector

from common.duplicate_filter.duplicate_filter import DuplicateFilter


class CountRedirector(Redirector):
    def __init__(self, recv_queue, send_queue, master_send_queue, callback, callback_eof, status_queue,
                 data_cluster_write, data_cluster_read):
        self.send_queue = send_queue
        self.callback = callback
        self.callback_eof = callback_eof

        Redirector.__init__(self, recv_queue, [send_queue], master_send_queue, status_queue, data_cluster_write,
                            data_cluster_read)

    def data_received(self, data):
        [connection_id, message_id, date, latitude, longitude, result] = data.split(",")
        if self.duplicate_filter.message_exists(connection_id, message_id):
            print("Duplicated message: " + message_id)
            return
        self.callback(result)
        self.duplicate_filter.insert_message(connection_id, message_id, data)

    def eof_received(self):
        self.callback_eof()

    def send_data(self, positives, deceased):
        msg = str(uuid.uuid4()) + str(positives) + "," + str(deceased)
        self.redirect_data(msg, self.send_queue)
