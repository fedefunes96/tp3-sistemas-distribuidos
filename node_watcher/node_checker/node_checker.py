from worker_manager.worker_manager import WorkerManager
from worker.worker import Worker
import time
from communication.message_types import DEAD, FINISHED
from config_reader.config_reader import ConfigReader

IDLE_TIME_DEAD = 60 #1 minute

class NodeChecker:
    def __init__(self, update_queue, dead_queue, raise_queue, config_file):
        self.update_queue = update_queue
        self.dead_queue = dead_queue
        self.raise_queue = raise_queue
        self.worker_manager = WorkerManager()
        self.dead_workers = []

        self.initialize_workers(config_file)
    
    def start(self):
        while True:
            actual_time = time.time()

            try:
                [status, worker_id, worker_type] = self.update_queue.get_nowait()

                if status == FINISHED:
                    pass

                if not self.worker_manager.worker_exists(worker_id):
                    print("Adding node: {} {}".format(worker_id, worker_type))
                    self.worker_manager.add_worker(worker_id, worker_type)
                else:
                    print("Updating node: {} {} {}".format(worker_id, worker_type, status))
                    self.worker_manager.update_timestamp_worker(
                        worker_id,
                        actual_time
                    )

                #Status says process is dead
                if status == DEAD:
                    node = self.worker_manager.remove_worker(
                        worker_id,
                        worker_type
                    )
                    print("Sending dead node to raise: {} {}".format(node.id, node.type))
                    self.dead_queue.put([node.id, node.type])
            except:
                pass
            finally:
                #What happens if Watcher (Status checker) dies?
                self.check_all_nodes(actual_time)
            
            self.incorporate_raised_workers()

    def incorporate_raised_workers(self):
        try:
            [worker_id, worker_type] = self.raise_queue.get_nowait()
            
            if not self.worker_manager.worker_exists(worker_id):
                print("Adding node: {} {}".format(worker_id, worker_type))
                self.worker_manager.add_worker(worker_id, worker_type)
        except:
            #There are no nodes to incorporate
            pass

    def check_all_nodes(self, actual_time):      
        dead_nodes = self.check_dead_nodes(actual_time)

        for node in dead_nodes:
            print("Sending dead nodes to raise: {} {}".format(node.id, node.type))
            self.dead_queue.put([node.id, node.type])

    def check_dead_nodes(self, actual_time):
        workers = self.worker_manager.remove_older_than_time(
            actual_time - IDLE_TIME_DEAD
        )

        return workers

    def initialize_workers(self, config_file):
        initial_workers = ConfigReader().parse_from_file(config_file)
        print("Initializing workers")
        for worker_id, worker_type in initial_workers.items():
            print("Added from config: {} {}".format(worker_id, worker_type))
            self.worker_manager.add_worker(worker_id, worker_type)
