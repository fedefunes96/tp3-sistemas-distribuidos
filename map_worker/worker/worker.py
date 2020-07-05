import csv
from map_controller.map_controller import MapController
from named_point.named_point import NamedPoint
from point.point import Point
from protocol_initialize.protocol_initialize import ProtocolInitialize

class Worker:
    def __init__(self, recv_queue, send_queue, master_queue, recv_init_queue):
        self.map_controller = MapController(
            recv_queue,
            send_queue,
            master_queue,
            self.process_data
        )

        self.initialize_protocol = ProtocolInitialize(
            recv_init_queue,
            self.process_places
        )

        self.places = []

    def process_places(self, region, latitude, longitude):
        point = NamedPoint(region, longitude, latitude)
        self.places.append(point)

    def start(self):
        self.initialize_protocol.start_connection()
        print("All places received")
        self.map_controller.start()

    def process_data(self, latitude, longitude):
        point = Point(longitude, latitude)

        return point.closest_point(self.places).name        
