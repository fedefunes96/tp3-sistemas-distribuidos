import pika

from middleware.receiver import Receiver

class DistributedWorkReceiver(Receiver):
    def initialize_channel(self):
        self.channel.queue_declare(queue=self.from_where, durable=True)

        self.channel.basic_qos(prefetch_count=1) 

        self.channel.basic_consume(
            queue=self.from_where,
            on_message_callback=self.data_received
        )       
