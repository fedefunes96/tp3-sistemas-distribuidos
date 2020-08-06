import pika
import sys
import random
import time

class TopicSender:
    def __init__(self, channel, topic):
        self.channel = channel
        self.topic = topic

        self.channel.exchange_declare(exchange=self.topic, exchange_type='fanout')

    def send(self, msg_type, msg):
        self.channel.basic_publish(
            exchange=self.topic,
            routing_key='',
            body=msg,
            properties=pika.BasicProperties(
                type=msg_type
            )
        )
