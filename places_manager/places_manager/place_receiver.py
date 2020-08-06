from protocol.receiver_protocol import ReceiverProtocol
from secure_data.secure_data import SecureData
from protocol.requester_protocol import RequesterProtocol
from state_saver.state_saver import StateSaver

import json

STAGE = "place_receiver"

class PlaceReceiver:
    def __init__(self, recv_queue, recv_request_queue, cluster_w_dir, cluster_r_dir):
        self.cluster_w_dir = cluster_w_dir
        self.cluster_r_dir = cluster_r_dir

        self.recv_request_queue = recv_request_queue

        self.state_saver = StateSaver(STAGE, cluster_w_dir, cluster_r_dir)

        self.protocol = ReceiverProtocol(recv_queue, self.state_saver)

        self.cluster_reader = SecureData(cluster_w_dir, cluster_r_dir)

        self.places = {}

    def start(self):
        load = self.state_saver.load_state("STATE")

        if load != None:
            [conn_id, state] = json.loads(load)

            if state == "RESTART":    
                print("Starting to receive places")
                conn_id = self.protocol.start_connection(
                    self.data_read,
                    #self.process_results,
                    self.load_data,
                    self.reset_data,
                    self.save_data      
                )
                print("Starting to accept requests")
                self.protocol_requester = RequesterProtocol(
                    self.recv_request_queue,
                    self.state_saver
                )

                self.protocol_requester.start_connection(
                    conn_id
                )
            elif state == "REQUESTER":
                print("Starting to accept requests")
                self.protocol_requester = RequesterProtocol(
                    self.recv_request_queue,
                    self.state_saver
                )

                self.protocol_requester.start_connection(
                    conn_id
                )
        else:    
            print("Starting to receive places")
            conn_id = self.protocol.start_connection(
                self.data_read,
                #self.process_results,
                self.load_data,
                self.reset_data,
                self.save_data      
            )
            print("Starting to accept requests")
            self.protocol_requester = RequesterProtocol(
                self.recv_request_queue,
                self.state_saver
            )

            self.protocol_requester.start_connection(
                conn_id
            )
    
    def load_data(self, places):
        self.places = places

    def reset_data(self):
        self.places = {}

    def save_data(self):
        return self.places

    def data_read(self, conn_id, place, latitude, longitude):
        self.places[place] = (latitude, longitude)
        
        self.cluster_reader.write_to_file(conn_id, "places.txt", json.dumps(self.places))
        print("Write finished")
