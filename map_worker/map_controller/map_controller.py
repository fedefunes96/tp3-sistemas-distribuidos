import uuid
import json

from redirector.redirector import Redirector
from state_saver.state_saver import StateSaver

class MapController(Redirector):
    def __init__(self, recv_queue, send_queues, master_send_queue, apply_func, status_queue, global_saver, single_saver, my_id):
        self.apply_func = apply_func
        self.send_queues = send_queues
        self.my_id = my_id
        self.state_saver = global_saver

        Redirector.__init__(self,
            recv_queue,
            send_queues,
            master_send_queue,
            status_queue,
            single_saver,
            my_id
        )

    def data_received(self, data):
        [connection_id, message_id, date, latitude, longitude, result] = data.split(",")

        if self.state_saver.is_duplicated(connection_id, message_id):
            print("Duplicated message: {}".format(message_id))
            return

        if result != "positivi":
            return

        place = self.apply_func(float(latitude), float(longitude))

        print("Place determined: {}".format(place))

        new_data = [connection_id, message_id, place]
        self.redirect_data(json.dumps(new_data), self.send_queues[0])
        #Dont need to save anything more than messages
        self.state_saver.save_state(connection_id, message_id, '')
        print("Data sent")
