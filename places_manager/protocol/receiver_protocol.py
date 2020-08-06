from middleware.connection import Connection
from communication.message_types import NORMAL, EOF
from middleware.secure_connection.secure_direct_receiver import SecureDirectReceiver
from state_saver.state_saver import StateSaver
import json

class ReceiverProtocol:
    def __init__(self, recv_queue, state_saver):
        self.connection = Connection()

        self.receiver = SecureDirectReceiver(recv_queue, self.connection)

        self.state_saver = state_saver

        self.connection_id = None 
    
    def start_connection(
        self,
        callback,
        #callback_eof,
        callback_load,
        callback_reset,
        callback_save        
    ):
        print("Starting to receive places")
        self.callback = callback
        #self.callback_eof = callback_eof
        self.callback_load = callback_load
        self.callback_reset = callback_reset
        self.callback_save = callback_save

        self.receiver.start_receiving(self.data_read)

        return self.connection_id

    def data_read(self, msg_type, msg):
        print("Msg received" + msg)

        if msg_type == NORMAL:
            [connection_id, message_id, region, latitude, longitude] = msg.split(",")
        else:
            [connection_id, message_id, eof] = msg.split(",")

        if self.state_saver.is_duplicated(connection_id, message_id):
            print("Duplicated message: {}".format(msg))
            return

        if connection_id != self.connection_id:
            last_state = self.state_saver.load_state(connection_id)

            if last_state is not None:
                self.callback_load(json.loads(last_state))
            else:
                self.callback_reset()

            self.connection_id = connection_id

        if msg_type == EOF:
            #self.callback_eof()
            self.receiver.close()
            self.state_saver.save_state("STATE", "", json.dumps([self.connection_id, "REQUESTER"]))
        else:
            self.callback(connection_id, region, latitude, longitude)

        data_to_save = self.callback_save()

        self.state_saver.save_state(connection_id, message_id, data_to_save)        
