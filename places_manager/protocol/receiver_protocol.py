from middleware.connection import Connection
from communication.message_types import NORMAL, EOF
#from middleware.secure_connection.secure_topic_receiver import SecureTopicReceiver
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver

class ReceiverProtocol:
    def __init__(self, recv_queue):
        self.connection = Connection()

        #self.receiver = self.connection.create_direct_receiver(recv_queue)

        #Should use direct receiver, dont need to use topic
        self.receiver = SecureDirectReceiver(recv_queue, self.connection)
    
    def start_connection(self, callback, callback_eof):
        print("Starting to receive places")
        self.callback = callback
        self.callback_eof = callback_eof

        self.receiver.start_receiving(self.data_read)

    def data_read(self, msg_type, msg):
        if msg_type == EOF:
            print("Eof received")
            self.callback_eof()
        else:
            print("Place received: {}".format(msg))
            [conn_id, msg_id, region, latitude, longitude] = msg.split(",")
            self.callback(conn_id, region, latitude, longitude)
