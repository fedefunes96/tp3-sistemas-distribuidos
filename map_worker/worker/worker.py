import csv
from map_controller.map_controller import MapController
from named_point.named_point import NamedPoint
from point.point import Point
from protocol_initialize.protocol_initialize import ProtocolInitialize
from secure_data.secure_data import SecureData
import json

class Worker:
    def __init__(
        self,
        recv_queue,
        send_queue,
        master_queue,
        recv_init_queue,
        status_queue,
        data_cluster_write,
        data_cluster_read
    ):
        self.map_controller = MapController(
            recv_queue,
            send_queue,
            master_queue,
            self.process_data,
            status_queue,
            data_cluster_write,
            data_cluster_read
        )

        self.initialize_protocol = ProtocolInitialize(
            recv_init_queue,
            self.process_places
        )

        self.cluster_reader = SecureData(data_cluster_write, data_cluster_read)

        self.places = []

    def process_places(self, region, longitude, latitude):
        point = NamedPoint(region, longitude, latitude)
        self.places.append(point)
    
    def read_places(self, conn_id):
        print("Reading places from {}".format(conn_id))
        result = self.cluster_reader.read_file(conn_id, "places.txt")

        places = json.loads(result)

        #for place in places:
        #    self.process_places(place[0], float(place[1]), float(place[2]))

        for place in places:
            print("{} {} {}".format(place, float(places[place][0]), float(places[place][1])))
            self.process_places(place, float(places[place][0]), float(places[place][1]))

    def start(self):
        #Block until places has been saved
        conn_id = self.initialize_protocol.start_connection()
        #Read places
        self.read_places(conn_id)
        print("All places received")
        self.map_controller.start()

    def process_data(self, latitude, longitude):
        point = Point(longitude, latitude)

        return point.closest_point(self.places).name        
