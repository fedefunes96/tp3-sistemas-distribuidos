import json
from middleware.connection import Connection
from communication.message_types import RESTART
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver
import time
from state_saver.state_saver import StateSaver

class Coordinator:
    def __init__(self, recv_queue, data_cluster_write, data_cluster_read):
        self.connection = Connection()
        self.state_saver = StateSaver(
            "coordinator_" + recv_queue,
            data_cluster_write,
            data_cluster_read
        )

        self.recv_queue = recv_queue
    
    def wait_to_work(self):
        self.receiver = SecureDirectReceiver(self.recv_queue, self.connection)
        self.receiver.start_receiving(self.receive_to_work)

    def receive_to_work(self, msg_type, conn_id):
        #Check duplicates
        if self.state_saver.is_duplicated(conn_id, msg_type):
            print("Duplicated message: {} {}".format(conn_id, msg_type))
            return

        
        print("Receive to start working")

        if msg_type == RESTART:
            self.receiver.close()

        self.state_saver.save_state(conn_id, msg_type, ".")