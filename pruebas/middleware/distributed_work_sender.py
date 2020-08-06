import pika
import sys
import random
import time

class DistributedWorkSender:
    def __init__(self, channel, where):
        self.channel = channel
        self.where = where

        self.channel.queue_declare(queue=self.where, durable=True)

    def send(self, msg_type, msg):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.where,
            body=msg,
            properties=pika.BasicProperties(
                delivery_mode=2,
                type=msg_type
            )
        )
