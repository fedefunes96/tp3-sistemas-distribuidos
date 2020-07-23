import pika

from middleware.receiver import Receiver

class RpcReceiver(Receiver):
    def data_received(self, ch, method, properties, body):
        self.callback(properties.reply_to, properties.correlation_id, body.decode('utf-8'))
        self.send_ack(method)

        if not self.running:
            self.channel.close()

    def initialize_channel(self):
        self.channel.queue_declare(queue=self.from_where, durable=True)

        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(
            queue=self.from_where,
            on_message_callback=self.data_received
        )
    
    def reply(self, id, reply_to, msg):
        self.channel.basic_publish(
            exchange='',
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id = id),
            body=str(msg)
        )

    def restart_queue(self):
        #Restart queue if it exists
        try:
            self.channel.delete_queue(self.from_where)
            self.channel.queue_declare(queue=self.from_where, durable=True)
        except:
            pass
