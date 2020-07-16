import time
from worker_manager.invalid_worker_type import InvalidWorkerType
from communication.worker_types import WORKER_TYPES

class Worker:
    def __init__(self, worker_id, worker_type):
        if worker_type not in WORKER_TYPES:
            raise InvalidWorkerType()

        self.id = worker_id
        self.type = worker_type
        self.timestamp = time.time()
    
    def update_timestamp(self, timestamp)
        self.timestamp = timestamp

    def __eq__(self, other): 
        if not isinstance(other, Worker):
            return NotImplemented

        return self.id == other.id
