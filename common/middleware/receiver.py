import pika
import sys
import random
import time

class Receiver:
    def __init__(self, channel, from_where):
        self.channel = channel
        self.from_where = from_where

        self.initialize_channel()

    def initialize_channel(self):
        raise NotImplementedError

    def start_receiving(self, callback):
        self.callback = callback
        self.running = True
        self.channel.start_consuming()
    
    def data_received(self, ch, method, properties, body):
        self.callback(properties.type, body.decode('utf-8'))
        self.send_ack(method)

        if not self.running:
            print("Closing channel")
            self.channel.close()

    def send_ack(self, method):
        self.channel.basic_ack(delivery_tag = method.delivery_tag)

    def close(self):
        self.running = False
