import uuid

from redirector.redirector import Redirector
from state_saver.state_saver import StateSaver

STAGE = "map_worker"

class MapController(Redirector):
    def __init__(self, recv_queue, send_queues, master_send_queue, apply_func, status_queue, data_cluster_write,
                 data_cluster_read):
        self.apply_func = apply_func
        self.send_queues = send_queues
        self.state_saver = StateSaver(STAGE, data_cluster_write, data_cluster_read)

        Redirector.__init__(self, recv_queue, send_queues, master_send_queue, status_queue)

    def data_received(self, data):
        [connection_id, message_id, date, latitude, longitude, result] = data.split(",")

        if self.state_saver.is_duplicated(connection_id, message_id):
            print("Duplicated message: {}".format(msg))
            return

        if result != "positivi":
            return

        place = self.apply_func(float(latitude), float(longitude))

        print("Place determined: {}".format(place))

        #new_data = connection_id + "," + str(uuid.uuid4()) + "," + place
        new_data = connection_id + "," + message_id + "," + place
        self.redirect_data(new_data, self.send_queues[0])
        #Dont need to save anything more than messages
        self.state_saver.save_state(connection_id, message_id, '')
        print("Data sent")
