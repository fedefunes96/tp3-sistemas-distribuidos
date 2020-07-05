from middleware.connection import Connection
import json

from communication.message_types import EOF, TOP_CITIES, DATE_RESULTS, TOTAL_COUNT

class Protocol:
    def __init__(self, recv_queue):
        self.connection = Connection()

        self.expected = 3
        self.actual = 0

        self.receiver = self.connection.create_direct_receiver(recv_queue)

    def start_connection(self, callback_top, callback_date, callback_count):
        self.callback_top = callback_top
        self.callback_date = callback_date
        self.callback_count = callback_count

        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            self.actual += 1

            if self.actual == self.expected:
                self.connection.close()
        elif msg_type == TOP_CITIES:
            self.callback_top(json.loads(msg))
        elif msg_type == DATE_RESULTS:
            self.callback_date(json.loads(msg))
        elif msg_type == TOTAL_COUNT:
            self.callback_count(float(msg))