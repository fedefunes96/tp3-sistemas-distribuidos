from protocol.receiver_protocol import ReceiverProtocol
from secure_data.secure_data import SecureData
import json

class PlaceReceiver:
    def __init__(self, recv_queue, accept_request_queue, cluster_w_dir, cluster_r_dir):
        self.protocol = ReceiverProtocol(recv_queue)

        self.cluster_reader = SecureData(cluster_w_dir, cluster_r_dir)

        self.accept_request_queue = accept_request_queue

        self.places = []

    def start(self):
        self.protocol.start_connection(self.data_read, self.process_results)

    def data_read(self, place, latitude, longitude):
        #Receive a place, save it in storage
        self.places.append((place, latitude, longitude))
        self.cluster_reader.write_to_file("tmp", "places.txt", json.dumps(self.places))
        print("Write finished")
        #pass
    
    def process_results(self):
        #Let the requester know that it can answer messages from map workers
        self.accept_request_queue.put(0)
