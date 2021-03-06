from master_controller.protocol.protocol import Protocol

class MasterController:
    def __init__(self, recv_queue, send_queue, total_workers, status_queue):
        self.protocol = Protocol(recv_queue, send_queue, total_workers, status_queue)

    def start(self):
        self.protocol.start_connection()
