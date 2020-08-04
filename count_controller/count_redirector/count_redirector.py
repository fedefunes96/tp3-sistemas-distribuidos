from redirector.redirector import Redirector

from state_saver.state_saver import StateSaver

STAGE = "count_worker"

class CountRedirector(Redirector):
    def __init__(
        self,
        recv_queue,
        send_queue,
        master_send_queue,
        callback,
        callback_eof,
        status_queue,
        data_cluster_write,
        data_cluster_read,
        worker_id,
        callback_load,
        callback_reset,
        callback_save
    ):
        self.send_queue = send_queue
        self.callback = callback
        self.callback_eof = callback_eof
        self.callback_load = callback_load
        self.callback_reset = callback_reset
        self.callback_save = callback_save

        self.connection_id = None
        self.worker_id = worker_id

        self.state_saver = StateSaver(STAGE, data_cluster_write, data_cluster_read)

        Redirector.__init__(self, recv_queue, [send_queue], master_send_queue, status_queue)

    def data_received(self, data):
        [connection_id, message_id, date, latitude, longitude, result] = data.split(",")

        if self.state_saver.is_duplicated(connection_id, message_id):
            print("Duplicated message: {}".format(msg))
            return

        if connection_id != self.connection_id:
            old_data = self.state_saver.load_state(connection_id)
            if old_data is not None:
                self.callback_load(old_data)
            else:
                self.callback_reset()

            self.connection_id = connection_id

        self.callback(result)

        data_to_save = self.callback_save()

        self.state_saver.save_state(connection_id, message_id, data_to_save)

    def eof_received(self, msg):
        [connection_id, message_id, eof_msg] = msg.split(',')

        if self.state_saver.is_duplicated(connection_id, message_id):
            print("Duplicated message: {}".format(msg))
            return    

        if connection_id != self.connection_id:
            old_data = self.state_saver.load_state(connection_id)
            if old_data is not None:
                self.callback_load(old_data)
            else:
                self.callback_reset()

            self.connection_id = connection_id

        self.callback_eof()

        data_to_save = self.callback_save()

        self.state_saver.save_state(connection_id, message_id, data_to_save)        

    def send_data(self, positives, deceased):
        msg = self.connection_id + "," + self.worker_id + "," + str(positives) + "," + str(deceased)
        self.redirect_data(msg, self.send_queue)
