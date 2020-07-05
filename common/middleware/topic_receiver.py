import pika
import sys
import random
import time

class TopicReceiver:
    def __init__(self, channel, from_topic):
        self.channel = channel
        self.from_topic = from_topic

        self.channel.exchange_declare(exchange=from_topic, exchange_type='fanout')

        result = self.channel.queue_declare(queue='', durable=True)

        queue_name = result.method.queue

        self.channel.queue_bind(exchange=from_topic, queue=queue_name)

        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.data_received,
            auto_ack=True
        )    

    def start_receiving(self, callback):
        self.callback = callback
        self.channel.start_consuming()
    
    def data_received(self, ch, method, properties, body):
        self.callback(properties.type, body.decode('utf-8'))

    def close(self):
        self.channel.close()