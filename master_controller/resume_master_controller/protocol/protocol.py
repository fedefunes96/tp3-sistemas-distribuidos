from middleware.connection import Connection

from communication.message_types import NORMAL, EOF, STOP, FINISHED
from middleware.secure_connection.secure_direct_sender import SecureDirectSender
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver
from state_saver.state_saver import StateSaver

import json

RESUME_MSG_ID = "master_eof"

class Protocol:
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
        self.connection = Connection()

        self.worker_id = worker_id
        self.total_workers = total_workers
        self.pending_connections = total_workers
        self.receiver = SecureDirectReceiver(recv_queue, self.connection)
        self.sender = SecureDirectSender(send_queue, self.connection)
        self.status_sender = SecureDirectSender(status_queue, self.connection)

        self.send_queue = send_queue

        self.state_saver = StateSaver(self.worker_id, data_cluster_write, data_cluster_read)

        self.connection_id = None

    def start_connection(self):
        self.receiver.start_receiving(self.data_read)
        self.connection.close()

    def data_read(self, msg_type, msg):
        print("Msg received: {}".format(msg))
        if msg_type == STOP:
            self.receiver.close()
            self.sender.send(STOP, '')
            self.status_sender.send(FINISHED, FINISHED)
            return

        data_recv = json.loads(msg)

        [connection_id, message_id] = data_recv[:2]

        if self.state_saver.is_duplicated(connection_id, message_id):
            print("Duplicated message: {}".format(msg))
            return

        if connection_id != self.connection_id:
            old_data = self.state_saver.load_state(connection_id)

            if old_data is not None:                
                self.pending_connections = old_data
            else:
                self.pending_connections = self.total_workers

            self.connection_id = connection_id

        if msg_type == EOF:
            self.pending_connections -= 1

            if self.pending_connections == 0:
                data_recv[1] = RESUME_MSG_ID
                self.sender.send(EOF, json.dumps(data_recv))
                print("Ended processing")

        data_to_save = self.pending_connections

        self.state_saver.save_state(connection_id, message_id, data_to_save)
