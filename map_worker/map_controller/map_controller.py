import uuid

from redirector.redirector import Redirector

STAGE = "map_worker"

class MapController(Redirector):
    def __init__(self, recv_queue, send_queues, master_send_queue, apply_func, status_queue, data_cluster_write,
                 data_cluster_read):
        self.apply_func = apply_func
        self.send_queues = send_queues

        Redirector.__init__(self, recv_queue, send_queues, master_send_queue, status_queue, data_cluster_write,
                            data_cluster_read)

    def data_received(self, data):
        [connection_id, message_id, date, latitude, longitude, result] = data.split(",")

        if self.duplicate_filter.message_exists(connection_id, STAGE, message_id):
            print("Duplicated message: " + message_id)
            return

        if result != "positivi":
            return

        place = self.apply_func(float(latitude), float(longitude))

        print("Place determined: {}".format(place))

        #new_data = connection_id + "," + str(uuid.uuid4()) + "," + place
        new_data = connection_id + "," + message_id + "," + place
        self.redirect_data(new_data, self.send_queues[0])
        self.duplicate_filter.insert_message(connection_id, STAGE, message_id, ".")

        print("Data sent")
