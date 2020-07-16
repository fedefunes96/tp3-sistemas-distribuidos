from worker.worker import Worker

class WorkerManager:
    def __init__(self, types):
        self.workers = []
        self.types = types

    def worker_exists(self, worker_id):
        for worker in self.workers
            if worker.id == worker_id:
                return True
        
        return False
    
    def add_worker(self, worker_id, worker_type):
        self.workers.append(Worker(worker_id, worker_type))

    def update_timestamp_worker(self, worker_id, actual_time):
        for worker in self.workers:
            if worker.id == worker_id:
                worker.update_timestamp(actual_time)

    def remove_older_than_time(self, time):
        old_workers = [x for x in self.workers if x.timestamp < time]

        self.workers = [x for x in self.workers if x not in old_workers]

        return old_workers

    def get_total_workers(self):
        total_workers = {}

        for w_type in self.workers_type:
            total_workers[w_type] = len(self.workers_type[w_type])

        return total_workers

    def remove_worker(self, worker_id):
        for worker_type in self.workers_type:
            if worker_id in self.workers_type[worker_type]:
                self.workers_type[worker_type].remove(worker_id)
        
        self.workers_
