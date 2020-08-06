import pika

from middleware.receiver import Receiver

class TopicReceiver(Receiver):
    def initialize_channel(self):
        self.channel.exchange_declare(exchange=self.from_where, exchange_type='fanout')

        result = self.channel.queue_declare(queue='', durable=True)

        queue_name = result.method.queue

        self.channel.queue_bind(exchange=self.from_where, queue=queue_name)

        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.data_received
        )        
