from protocol.receiver_protocol import ReceiverProtocol
from secure_data.secure_data import SecureData
import json

class PlaceReceiver:
    def __init__(self, recv_queue, accept_request_queue, cluster_w_dir, cluster_r_dir):
        self.protocol = ReceiverProtocol(recv_queue)

        self.cluster_reader = SecureData(cluster_w_dir, cluster_r_dir)

        self.accept_request_queue = accept_request_queue

        self.places = {}
        #self.places = []

        self.conn_id = None

    def start(self):
        self.protocol.start_connection(self.data_read, self.process_results)

    def data_read(self, conn_id, place, latitude, longitude):
        #Receive a place, save it in storage
        if self.conn_id == None:
            self.conn_id = conn_id
        
        self.places[place] = (latitude, longitude)
        #self.places.append((place, latitude, longitude))
        
        self.cluster_reader.write_to_file(conn_id, "places.txt", json.dumps(self.places))
        print("Write finished")
    
    def process_results(self):
        #Let the requester know that it can answer messages from map workers
        self.accept_request_queue.put(self.conn_id)
