import pika
import sys
import random
import time

from middleware.connection import Connection
from communication.message_types import NORMAL, EOF

class Protocol:
    def __init__(self,
        queue_map,
        queue_date,
        queue_count,
        eof_map,
        eof_date,
        eof_count,
        topic_places
    ):
        self.connection = Connection()

        self.sender_map = self.connection.create_distributed_work_sender(queue_map)
        self.sender_date = self.connection.create_distributed_work_sender(queue_date)
        self.sender_count = self.connection.create_distributed_work_sender(queue_count)

        self.sender_places = self.connection.create_topic_sender(topic_places)

        self.eof_map = self.connection.create_direct_sender(eof_map)
        self.eof_date = self.connection.create_direct_sender(eof_date)
        self.eof_count = self.connection.create_direct_sender(eof_count)

    def process_places(self, region, latitude, longitude):
        message = region + "," + latitude + "," + longitude

        self.sender_places.send(NORMAL, message)
    
    def send_no_more_places(self):
        self.sender_places.send(EOF, "")

    def process(self, date, latitude, longitude, result):
        message = date + "," + latitude + "," + longitude + "," + result

        self.sender_map.send(NORMAL, message)
        self.sender_date.send(NORMAL, message)
        self.sender_count.send(NORMAL, message)

    def close(self):
        #self.sender_map.send(EOF, "")
        #self.sender_date.send(EOF, "")
        #self.sender_count.send(EOF, "")
        self.eof_map.send(EOF, "")
        self.eof_date.send(EOF, "")
        self.eof_count.send(EOF, "")

        self.connection.close()
