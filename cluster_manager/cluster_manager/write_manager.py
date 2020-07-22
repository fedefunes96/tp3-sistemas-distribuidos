import os
from shutil import copyfile
from writer.writer import Writer
from protocol.write_protocol import WriteProtocol
from communication.message_types import WRITE, APPEND

TMP_FILE_NAME = "tmp.txt"

class WriteManager:
    def __init__(self, folder, recv_queue, replicas_queues):
        self.folder = folder
        self.writer = Writer()
        self.protocol = WriteProtocol(recv_queue, replicas_queues)
        
    def start(self):
        self.protocol.start_receiving(
            self.requested_append,
            self.requested_write
        )
    
    def requested_write(self, folder_to_write, file_to_write, data):
        write_in = self.folder + "/" + folder_to_write + "/" + file_to_write
        tmp_file = self.folder + "/" + folder_to_write + "/" + TMP_FILE_NAME

        #Only one write request
        self.writer.write_file(write_in, tmp_file, data, 'w')

        return self.protocol.replicate_data(folder_to_write, file_to_write, data, WRITE)

    def requested_append(self, folder_to_write, file_to_write, data):
        write_in = self.folder + "/" + folder_to_write + "/" + file_to_write
        tmp_file = self.folder + "/" + folder_to_write + "/" + TMP_FILE_NAME

        try:
            copyfile(write_in, tmp_file)
        except FileNotFoundError:
            pass

        self.writer.write_file(write_in, tmp_file, 'a')

        return self.protocol.replicate_data(folder_to_write, file_to_write, data, APPEND)
