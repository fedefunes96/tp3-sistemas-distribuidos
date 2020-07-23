from protocol.receiver_protocol import ReceiverProtocol

class PlaceReceiver:
    def __init__(self, recv_queue, accept_request_queue):
        self.protocol = ReceiverProtocol(recv_queue)

        self.accept_request_queue = accept_request_queue

    def start(self):
        self.protocol.start_connection(self.data_read, self.process_results)

    def data_read(self, place, latitude, longitude):
        #Receive a place, save it in storage
        pass
    
    def process_results(self):
        #Let the requester know that it can answer messages from map workers
        self.accept_request_queue.put(0)
