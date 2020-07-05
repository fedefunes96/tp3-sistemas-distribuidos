import pika
import sys
import random
import time

class DirectReceiver:
    def __init__(self, channel, from_where):
        self.channel = channel
        self.from_where = from_where

        self.channel.queue_declare(queue=self.from_where)

    def start_receiving(self, callback):
        self.channel.basic_consume(
            queue=self.from_where,
            on_message_callback=self.data_received,
            auto_ack=True
        )

        self.callback = callback
        self.channel.start_consuming()
    
    def data_received(self, ch, method, properties, body):
        self.callback(properties.type, body.decode('utf-8'))

    def close(self):
        self.channel.close()