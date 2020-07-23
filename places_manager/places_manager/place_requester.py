from protocol.requester_protocol import RequesterProtocol
from communication.message_types import READY

class PlaceRequester:
    def __init__(self, recv_request_queue, accept_request_queue):
        self.protocol = RequesterProtocol(
            recv_request_queue
        )

        self.accept_request_queue = accept_request_queue

    def start(self):
        #Wait until receiver receives all places
        _tmp = self.accept_request_queue.get()

        self.protocol.start_connection(self.request_places_ready)

        #Return false if stopped gracefully
        return True

    def request_places_ready(self):
        return READY
