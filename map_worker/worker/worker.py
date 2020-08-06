import csv
from map_controller.map_controller import MapController
from named_point.named_point import NamedPoint
from point.point import Point
from protocol_initialize.protocol_initialize import ProtocolInitialize
from secure_data.secure_data import SecureData
import json
from state_saver.state_saver import StateSaver
from coordinator.coordinator import Coordinator

GLOBAL_STAGE = "map_worker"
COORDINATOR_STAGE = "coordinator_map_worker"

class Worker:
    def __init__(
        self,
        recv_queue,
        send_queue,
        master_queue,
        recv_init_queue,
        status_queue,
        data_cluster_write,
        data_cluster_read,
        my_id
    ):
        self.global_saver = StateSaver(GLOBAL_STAGE, data_cluster_write, data_cluster_read)
        self.single_saver = StateSaver(my_id, data_cluster_write, data_cluster_read)

        self.map_controller = MapController(
            recv_queue,
            send_queue,
            master_queue,
            self.process_data,
            status_queue,
            self.global_saver,
            self.single_saver,
            my_id
        )

        self.initialize_protocol = ProtocolInitialize(
            recv_init_queue,
            self.process_places
        )

        self.cluster_reader = SecureData(data_cluster_write, data_cluster_read)

        self.coordinator = Coordinator(
            my_id,
            data_cluster_write,
            data_cluster_read
        )

    def process_places(self, region, longitude, latitude):
        point = NamedPoint(region, longitude, latitude)
        self.places.append(point)
    
    def read_places(self, conn_id):
        print("Reading places from {}".format(conn_id))
        result = self.cluster_reader.read_file(conn_id, "places.txt")

        places = json.loads(result)

        # Restart places
        self.places = []
        for place in places:
            print("{} {} {}".format(place, float(places[place][0]), float(places[place][1])))
            self.process_places(place, float(places[place][0]), float(places[place][1]))

    def start(self):
        self.places = []
        state = self.single_saver.load_state("STATE")
        
        if state == "WAITING":
            #Wait for coordinator
            print("Waiting for coordinator")
            self.coordinator.wait_to_work()
            self.single_saver.save_state("STATE", "", "READY")
        else:
            #Block until places has been saved
            conn_id = self.initialize_protocol.start_connection()
            #Read places
            self.read_places(conn_id)
            print("All places received")      
            self.map_controller.start()

    def process_data(self, latitude, longitude):
        point = Point(longitude, latitude)
        return point.closest_point(self.places).name
