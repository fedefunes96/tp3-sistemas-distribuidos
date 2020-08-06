from middleware.connection import Connection
import json

from communication.message_types import EOF, TOP_CITIES, DATE_RESULTS, TOTAL_COUNT, STOP, FINISHED, RESTART 
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver
from middleware.secure_connection.secure_direct_sender import SecureDirectSender
from middleware.secure_connection.secure_rpc_sender import SecureRpcSender
from state_saver.state_saver import StateSaver

EXPECTED_EOF = 3
STAGE = "summary"

class Protocol:
    def __init__(
            self,
            recv_queue,
            status_queue,
            data_cluster_write,
            data_cluster_read,
            coordinator_queue
        ):
        self.connection = Connection()

        self.expected = EXPECTED_EOF
        self.actual = 0

        self.receiver = SecureDirectReceiver(recv_queue, self.connection)
        self.status_sender = SecureDirectSender(status_queue, self.connection)
        #self.coordinator_sender = SecureRpcSender(coordinator_queue, self.connection)
        self.coordinator_sender = SecureRpcSender(coordinator_queue, Connection())

        self.state_saver = StateSaver(STAGE, data_cluster_write, data_cluster_read)

        self.connection_id = None

    def start_connection(
        self,
        callback_top,
        callback_date,
        callback_count,
        callback_all_data,
        callback_load,
        callback_reset,
        callback_save        
    ):
        self.callback_top = callback_top
        self.callback_date = callback_date
        self.callback_count = callback_count
        self.callback_all_data = callback_all_data
        self.callback_load = callback_load
        self.callback_reset = callback_reset
        self.callback_save = callback_save

        if self.actual < self.expected:
            self.receiver.start_receiving(self.data_read)

        self.connection.close()

    def data_read(self, msg_type, msg):
        print("Msg received" + msg)

        if msg_type == STOP:
            self.receiver.close()
            self.status_sender.send(FINISHED, FINISHED)
            return

        data_recv = json.loads(msg)

        [connection_id, message_id] = data_recv[:2]

        if self.state_saver.is_duplicated(connection_id, message_id):
            print("Duplicated message: {}".format(msg))
            return

        if connection_id != self.connection_id:
            last_state = self.state_saver.load_state(connection_id)

            if last_state is not None:
                [old_data, actual_conns] = last_state
                
                self.actual = actual_conns
                self.callback_load(old_data)
            else:
                self.actual = 0
                self.callback_reset()

            self.connection_id = connection_id

        if msg_type == EOF:
            self.actual += 1

            if self.actual == self.expected:
                self.callback_all_data(self.connection_id)
                self.reset_coordinator()
                print("Ended processing")
        elif msg_type == TOP_CITIES:
            print("Received TOP CITIES")
            [data] = data_recv[2:]
            self.callback_top(json.loads(data))
        elif msg_type == DATE_RESULTS:
            print("Received DATE RESULTS")
            [data] = data_recv[2:]
            self.callback_date(json.loads(data))
        elif msg_type == TOTAL_COUNT:
            print("Received COUNT TOTAL")
            [data] = data_recv[2:]
            self.callback_count(data)

        data_to_save = [self.callback_save(), self.actual]

        self.state_saver.save_state(connection_id, message_id, data_to_save)

    def reset_coordinator(self):
        _tmp = self.coordinator_sender.send(json.dumps([self.connection_id, RESTART]))
        print("Received: {}".format(_tmp))