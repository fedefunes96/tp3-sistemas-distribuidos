from protocol.protocol import Protocol
from communication.message_types import READY, NOT_READY
from state_saver.state_saver import StateSaver

import json

STAGE = "coordinator"

class CoordinatorManager:
    def __init__(self,
        recv_queue,
        send_queues,
        data_cluster_write,
        data_cluster_read,
        place_manager_queue
    ):
        self.state_saver = StateSaver(STAGE, data_cluster_write, data_cluster_read)

        self.protocol = Protocol(recv_queue, send_queues, self.state_saver, place_manager_queue)
        self.working = False
        self.actual_conn = None

    def start(self):
        load = self.state_saver.load_state("STATE")

        if load != None:
            [conn_id, state] = json.loads(load)

            self.actual_conn = conn_id

            if state == "RESTART":    
                self.work_finished(conn_id)
            elif state == "BLOCKED":
                self.working = True

        self.protocol.start_receiving(
            self.work_finished,
            self.new_client
        )
    
    def new_client(self, conn_id):
        if conn_id == self.actual_conn:
            return READY
            
        if self.working:
            return NOT_READY

        self.working = True
        self.actual_conn = conn_id

        return READY

    def work_finished(self, conn_id):
        #Force place manager to restart its requester
        #and force every worker to restart
        self.protocol.restart_all_senders(conn_id)
        
        self.working = False
