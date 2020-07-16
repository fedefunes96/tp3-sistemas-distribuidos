from protocol.protocol import Protocol
from worker_manager.worker_manager import WorkerManager
from worker_manager.invalid_worker_type import InvalidWorkerType
from communication.worker_types import WORKER_TYPES, WORKER_MIN_NODES
from config_reader.config_reader import ConfigReader
from worker.worker import Worker
import time

INITIALIZE_TIME = 60 #1 minute
IDLE_TIME_DEAD = 60 #1 minute

class Watcher:
    def __init__(self, init_queue, config_file):
        self.protocol = Protocol(init_queue)
        self.worker_manager = WorkerManager()
        self.dead_workers = []
    
    def start(self, config_file):
        self.init_time = time.time()

        self.protocol.start_receiving(self.health_status_received)

    def health_status_received(self, worker_id, worker_type):
        actual_time = time.time()

        if not self.worker_manager.worker_exists(worker_id):
            self.worker_manager.add_worker(worker_id, worker_type)
        else:
            self.worker_manager.update_timestamp_worker(
                worker_id,
                actual_time
            )

    def check_all_nodes(self):
        #if not actual_time > self.init_time + INITIALIZE_TIME:
        #    return        
        actual_time = time.time()

        self.check_dead_nodes(actual_time)

        self.raise_missing_nodes()

    def check_dead_nodes(self, actual_time):
        workers = self.worker_manager.remove_older_than_time(
            actual_time - IDLE_TIME_DEAD
        )

        self.dead_workers.update(workers)

    def raise_missing_nodes(self):
        for worker in self.dead_workers:


    def initialize_workers(config_file):
        initial_workers = ConfigReader().parse_from_file(config_file)

        for worker_type in initial_workers:
            for number_workers in range(0, initial_workers[worker_type]):
                self.raise_up_worker(worker_type)

    def raise_up_worker(worker_type):
        #Raise up worker with init_queue to check if it comes up
        pass