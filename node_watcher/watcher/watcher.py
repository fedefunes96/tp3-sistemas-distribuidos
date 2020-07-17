from watcher.protocol.protocol import Protocol

class Watcher:
    def __init__(self, init_queue, update_queue):
        self.protocol = Protocol(init_queue)
        self.update_queue = update_queue
    
    def start(self):
        self.protocol.start_receiving(self.health_status_received)

    def health_status_received(self, worker_id, worker_type):
        self.update_queue.put([worker_id, worker_type])
