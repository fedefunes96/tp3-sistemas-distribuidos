class NodeRaiser:
    def __init__(self, dead_queue):
        self.dead_queue = dead_queue

    def start(self):
        while True:
            [worker_id, worker_type] = self.update_queue.get()
            
            self.raise_node(worker_id, worker_type)

    def raise_node(worker_id, worker_type)
        pass