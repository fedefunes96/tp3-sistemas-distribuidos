from middleware.connection import Connection
from communication.message_types import WRITE_OK, FAILED, APPEND, WRITE
from secure_data.exceptions.write_error import WriteError

class SecureData:
    def __init__(self, cluster_w_dir, cluster_r_dir):
        self.connection = Connection()

        self.sender_write = self.connection.create_rpc_sender(cluster_w_dir)
        self.sender_read = self.connection.create_rpc_sender(cluster_r_dir)
    
    def write_to_file(self, folder_to_write, file_to_write, data):
        print("Sending data: {}".format(data))
        msg = folder_to_write + "@@" + file_to_write + "@@" + data + "@@" + WRITE
        print("Sending msg: {}".format(msg))
        recv_msg = self.sender_write.send(msg)

        if recv_msg == FAILED:
            raise WriteError() 
    
    def append_to_file(self, folder_to_write, file_to_write, data):
        msg = folder_to_write + "@@" + file_to_write + "@@" + data + "@@" + APPEND

        recv_msg = self.sender_write.send(msg)

        if recv_msg == FAILED:
            raise WriteError() 
    
    def read_file(self, folder_to_read, file_to_read):
        msg = folder_to_read + "@@" + file_to_read

        return self.sender_read.send(msg)
