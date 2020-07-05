import pika
import sys
import random
import time

from middleware.direct_sender import DirectSender
from middleware.direct_receiver import DirectReceiver
from middleware.distributed_work_receiver import DistributedWorkReceiver
from middleware.distributed_work_sender import DistributedWorkSender
from middleware.topic_receiver import TopicReceiver
from middleware.topic_sender import TopicSender

class Connection:
    def __init__(self):
        self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='rabbitmq')
            )

    def reserve_queue_topic(self, topic, queue):
        channel = self.connection.channel()

        channel.exchange_declare(exchange=topic, exchange_type='fanout')

        channel.queue_declare(queue=queue, durable=True)

        channel.queue_bind(exchange=topic, queue=queue)

    def create_direct_sender(self, where):
        channel = self.connection.channel()

        return DirectSender(channel, where)
        
    def create_direct_receiver(self, from_where):
        channel = self.connection.channel()

        return DirectReceiver(channel, from_where)
    
    def create_distributed_work_sender(self, where):
        channel = self.connection.channel()

        return DistributedWorkSender(channel, where)   

    def create_distributed_work_receiver(self, from_where):
        channel = self.connection.channel()

        return DistributedWorkReceiver(channel, from_where)

    def create_topic_sender(self, where):
        channel = self.connection.channel()

        return TopicSender(channel, where)   
            
    def create_topic_receiver(self, from_where):
        channel = self.connection.channel()

        return TopicReceiver(channel, from_where)

    def close(self):
        self.connection.close()
