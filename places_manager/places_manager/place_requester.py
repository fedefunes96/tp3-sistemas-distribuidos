from protocol.requester_protocol import RequesterProtocol
from communication.message_types import READY

class PlaceRequester:
    def __init__(self, recv_request_queue, accept_request_queue, cluster_w_dir, cluster_r_dir):
        self.recv_request_queue = recv_request_queue

        self.accept_request_queue = accept_request_queue

        self.cluster_w_dir = cluster_w_dir
        self.cluster_r_dir = cluster_r_dir

        self.conn_id = None

    def start(self):
        #Wait until receiver receives all places
        self.conn_id = self.accept_request_queue.get()

        self.protocol = RequesterProtocol(
            self.recv_request_queue,
            self.cluster_w_dir,
            self.cluster_r_dir
        )

        self.protocol.start_connection(self.request_places_ready)

        #Return false if stopped gracefully
        return True

    def request_places_ready(self):
        return self.conn_id
