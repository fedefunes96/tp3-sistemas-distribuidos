from resume_master_controller.protocol.protocol import Protocol

class ResumeMasterController:
    def __init__(
        self,
        recv_queue,
        send_queue,
        total_workers,
        status_queue,
        worker_id,
        data_cluster_write,
        data_cluster_read        
    ):
        self.protocol = Protocol(
            recv_queue,
            send_queue,
            total_workers,
            status_queue,
            worker_id,
            data_cluster_write,
            data_cluster_read              
        )

    def start(self):
        self.protocol.start_connection()
