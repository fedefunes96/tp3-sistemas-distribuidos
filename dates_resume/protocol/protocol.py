import pika
import sys
import random
import time
import json

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF, STOP, FINISHED
from middleware.secure_connection.secure_direct_sender import SecureDirectSender
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver
from state_saver.state_saver import StateSaver

DATE_MSG_ID = "dates_resume_jan"
STAGE = "date_resume"
EOF_MSG_ID = "dates_resume_jan_eof"

class Protocol:
    def __init__(
        self,
        recv_queue,
        send_queue,
        status_queue,
        data_cluster_write,
        data_cluster_read
    ):
        self.connection = Connection()
        self.receiver = SecureDirectReceiver(recv_queue, self.connection)
        self.sender = SecureDirectSender(send_queue, self.connection)
        self.status_sender = SecureDirectSender(status_queue, self.connection)

        self.state_saver = StateSaver(STAGE, data_cluster_write, data_cluster_read)

        self.connection_id = None

    def start_connection(self,
        callback,
        callback_eof,
        callback_load,
        callback_reset,
        callback_save
    ):
        self.callback = callback
        self.callback_eof = callback_eof
        self.callback_load = callback_load
        self.callback_reset = callback_reset
        self.callback_save = callback_save

        self.receiver.start_receiving(self.data_read)

    def send_data(self, data):
        new_data = [self.connection_id, DATE_MSG_ID, json.dumps(data)]
        eof_to_send = [self.connection_id, EOF_MSG_ID]

        self.sender.send(NORMAL, json.dumps(new_data))
        self.sender.send(EOF, json.dumps(eof_to_send))

    def data_read(self, msg_type, msg):
        if msg_type == STOP:
            self.receiver.close()
            self.sender.send(STOP, "")
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
                self.callback_load(old_data)
            else:
                self.callback_reset()

            self.connection_id = connection_id

        if msg_type == EOF:
            print("Ended processing")
            self.callback_eof()
        else:
            [date, result] = data_recv[2:]
            self.callback(date, result)

        data_to_save = self.callback_save()

        self.state_saver.save_state(connection_id, message_id, data_to_save)
