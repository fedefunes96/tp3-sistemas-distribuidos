import pika
import uuid
import time
from threading import Thread

from middleware.exceptions.rpc_timeout import RPCTimeout

class RpcSender:
    def __init__(self, connection, where):
        self.connection = connection
        self.channel = self.connection.channel()

        self.where = where

        result = self.channel.queue_declare(queue='', exclusive=True)

        #Declaring this queue allows Server to answer when it comes up
        self.channel.queue_declare(queue=where, durable=True)

        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def send(self, msg, timeout=None):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.where,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=msg
        )

        start_time = time.time()

        while self.response is None:                
            if timeout != None and (start_time + timeout) < time.time():
                raise RPCTimeout()

            self.connection.process_data_events()

        return self.response.decode('utf-8')
