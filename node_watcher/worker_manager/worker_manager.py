from worker_manager.invalid_worker_type import InvalidWorkerType

class WorkerManager:
    def __init__(self, types):
        self.workers = {}
        self.types = types
    
    def add_worker(worker_type, status_queue):
        if worker_type not in self.types:
            raise InvalidWorkerType()

        if worker_type not in self.workers:
            self.workers[worker_type] = []

        self.workers[worker_type].append(status_queue)

    def get_total_workers(self):
        total_workers = {}

        for w_type in self.workers:
            total_workers[w_type] = len(self.workers[w_type])

        return total_workers

    def remove_worker(status_queue):
        for worker_type in self.workers:
            if status_queue in self.workers[worker_type]:
                self.workers[worker_type].remove(status_queue)
