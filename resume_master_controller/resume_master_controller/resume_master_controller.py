from protocol.protocol import Protocol

class ResumeMasterController:
    def __init__(self, recv_queue, send_queue, total_workers):
        self.protocol = Protocol(recv_queue, send_queue, total_workers)

    def start(self):
        self.protocol.start_connection()
