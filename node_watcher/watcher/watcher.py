from protocol.protocol import Protocol
from worker_manager.worker_manager import WorkerManager
from worker_manager.invalid_worker_type import InvalidWorkerType
from communication.worker_types import WORKER_TYPES, WORKER_MIN_NODES
from config_reader.config_reader import ConfigReader

class Watcher:
    def __init__(self, init_queue, config_file):
        self.protocol = Protocol(init_queue)
        self.worker_manager = WorkerManager()
    
    def start(self, config_file):

        self.initialize_workers(config_file)

        while True:
            self.protocol.receive_new_workers(self.received_new_worker)

    def received_new_worker(self, worker_type, status_queue):
        # (TODO) Save in cluster
        try:
            self.worker_manager.add_worker(worker_type, status_queue)
        except InvalidWorkerType:
            pass

    def initialize_workers(config_file):
        initial_workers = ConfigReader().parse_from_file(config_file)

        for worker_type in initial_workers:
            for number_workers in range(0, initial_workers[worker_type]):
                self.raise_up_worker(worker_type)

    def raise_up_worker(worker_type):
        #Raise up worker with init_queue to check if it comes up
        pass