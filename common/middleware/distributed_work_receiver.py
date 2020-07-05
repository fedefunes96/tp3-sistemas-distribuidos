import pika
import sys
import random
import time

class DistributedWorkReceiver:
    def __init__(self, channel, from_where):
        self.channel = channel
        self.from_where = from_where

        self.channel.queue_declare(queue=self.from_where, durable=True)

        self.channel.basic_qos(prefetch_count=1)

    def start_receiving(self, callback):
        self.channel.basic_consume(
            queue=self.from_where,
            on_message_callback=self.data_received
        )

        self.callback = callback
        self.channel.start_consuming()
    
    def data_received(self, ch, method, properties, body):
        self.callback(method, properties.type, body.decode('utf-8'))

    def send_ack(self, method):
        self.channel.basic_ack(delivery_tag = method.delivery_tag)

    def close(self):
        self.channel.close()