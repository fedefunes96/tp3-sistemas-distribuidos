from watcher.protocol.protocol import Protocol

class Watcher:
    def __init__(self, init_queue, update_queue):
        self.protocol = Protocol(init_queue)
        self.update_queue = update_queue
    
    def start(self):
        print("Starting to receive Health status")
        self.protocol.start_receiving(self.health_status_received)

    def health_status_received(self, status, worker_id, worker_type):
        print("Health status received: {} {} {}".format(status, worker_id, worker_type))
        self.update_queue.put([status, worker_id, worker_type])
