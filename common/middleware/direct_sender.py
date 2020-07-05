import pika
import sys
import random
import time

class DirectSender:
    def __init__(self, channel, where):
        self.channel = channel
        self.where = where

        self.channel.queue_declare(queue=self.where)

    def send(self, msg_type, msg):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.where,
            properties=pika.BasicProperties(
                delivery_mode=2,
                type=msg_type
            ),
            body=msg
        )
