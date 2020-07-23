import csv
from map_controller.map_controller import MapController
from named_point.named_point import NamedPoint
from point.point import Point
from protocol_initialize.protocol_initialize import ProtocolInitialize
from duplicate_filter.duplicate_filter import DuplicateFilter


class Worker:
    def __init__(self, recv_queue, send_queue, master_queue, recv_init_queue, status_queue, data_cluster_write, data_cluster_read):
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
            self.process_places,
            data_cluster_write,
            data_cluster_read
        )
        self.duplicate_filter = DuplicateFilter(data_cluster_write, data_cluster_read)
        self.places = []

    def process_places(self, msg):
        [connection_id, message_id, region, longitude, latitude] = msg.split(",")
        if self.duplicate_filter.message_exists(connection_id, message_id):
            print("Duplicated message: " + message_id)
            return
        point = NamedPoint(region, float(longitude), float(latitude))
        self.places.append(point)
        self.duplicate_filter.insert_message(connection_id, message_id, msg)

    def start(self):
        self.initialize_protocol.start_connection()
        print("All places received")
        self.map_controller.start()

    def process_data(self, latitude, longitude):
        point = Point(longitude, latitude)

        return point.closest_point(self.places).name        
