from worker_manager.worker_manager import WorkerManager
from worker.worker import Worker
import time

IDLE_TIME_DEAD = 60 #1 minute

class NodeChecker:
    def __init__(self, update_queue, dead_queue):
        self.update_queue = update_queue
        self.dead_queue = dead_queue
        self.worker_manager = WorkerManager()
        self.dead_workers = []
    
    def start(self):
        while True:
            actual_time = time.time()

            try:
                [worker_id, worker_type] = self.update_queue.get_nowait()

                if not self.worker_manager.worker_exists(worker_id):
                    self.worker_manager.add_worker(worker_id, worker_type)
                else:
                    self.worker_manager.update_timestamp_worker(
                        worker_id,
                        actual_time
                    )
            finally:
                #What happens if Watcher (Status checker) dies?
                self.check_all_nodes(actual_time)

    def check_all_nodes(self, actual_time):      
        dead_nodes = self.check_dead_nodes(actual_time)

        for node in dead_nodes:
            self.dead_queue.put([node.id, node.type])

    def check_dead_nodes(self, actual_time):
        workers = self.worker_manager.remove_older_than_time(
            actual_time - IDLE_TIME_DEAD
        )

        self.dead_workers.update(workers)
