import csv
from map_controller.map_controller import MapController
from named_point.named_point import NamedPoint
from point.point import Point
from protocol_initialize.protocol_initialize import ProtocolInitialize
from secure_data.secure_data import SecureData
import json

class Worker:
    def __init__(self, recv_queue, send_queue, master_queue, send_init_queue, status_queue):
        self.map_controller = MapController(
            recv_queue,
            send_queue,
            master_queue,
            self.process_data,
            status_queue
        )

        self.initialize_protocol = ProtocolInitialize(
            send_init_queue,
            self.process_places
        )

        self.cluster_reader = SecureData()

        self.places = []

    def process_places(self, region, latitude, longitude):
        point = NamedPoint(region, longitude, latitude)
        self.places.append(point)
    
    def read_places(self):
        result = self.cluster_reader.read_file("tmp", "places.txt")

        for row in json.loads(result):
            self.process_places(row[0], float(row[1]), float(row[2]))

    def start(self):
        #Block until places has been saved
        self.initialize_protocol.start_connection()
        #Read places
        self.read_places()
        #print("All places received")
        self.map_controller.start()

    def process_data(self, latitude, longitude):
        point = Point(longitude, latitude)

        return point.closest_point(self.places).name        
