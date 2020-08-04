from middleware.connection import Connection
import json

from communication.message_types import EOF, TOP_CITIES, DATE_RESULTS, TOTAL_COUNT, STOP, FINISHED
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver
from middleware.secure_connection.secure_direct_sender import SecureDirectSender

EXPECTED_EOF = 3

class Protocol:
    def __init__(self, recv_queue, status_queue):
        self.connection = Connection()

        self.expected = EXPECTED_EOF
        self.actual = 0

        self.receiver = SecureDirectReceiver(recv_queue, self.connection)
        self.status_sender = SecureDirectSender(status_queue, self.connection)

    def start_connection(self, callback_top, callback_date, callback_count, callback_all_data):
        self.callback_top = callback_top
        self.callback_date = callback_date
        self.callback_count = callback_count
        self.callback_all_data = callback_all_data

        if self.actual < self.expected:
            self.receiver.start_receiving(self.data_read)

        self.connection.close()

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            self.add_already_read()
        elif msg_type == TOP_CITIES:
            print("Received TOP CITIES")
            self.callback_top(msg)
        elif msg_type == DATE_RESULTS:
            print("Received DATE RESULTS")
            self.callback_date(msg)
        elif msg_type == TOTAL_COUNT:
            print("Received COUNT TOTAL")
            self.callback_count(msg)
        elif msg_type == STOP:
            print("Received STOP")
            self.receiver.close()
            self.status_sender.send(FINISHED, FINISHED)

    def add_already_read(self):
        self.actual += 1
        if self.actual == self.expected:
            self.finish_processing()

    def finish_processing(self):
        self.callback_all_data()
        self.actual = 0

