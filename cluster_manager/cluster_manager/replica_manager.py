import os
from shutil import copyfile
from writer.writer import Writer
from communication.message_types import WRITE_OK, FAILED
from protocol.replica_protocol import ReplicaProtocol

TMP_FILE_NAME = "tmp_rep.txt"

class ReplicaManager:
    def __init__(self, folder, recv_queue):
        self.folder = folder
        self.writer = Writer()
        self.protocol = ReplicaProtocol(recv_queue)
        
    def start(self):
        self.protocol.start_receiving(
            self.requested_replica_append,
            self.requested_replica_write
        )
    
    def requested_replica_append(self, folder_to_write, file_to_write, data):
        write_in = self.folder + "/" + folder_to_write + "/" + file_to_write
        tmp_file = self.folder + "/" + folder_to_write + "/" + TMP_FILE_NAME
        
        try:
            os.makedirs(self.folder + "/" + folder_to_write)
            print("Directory created (Didnt exist)")
        except OSError as error:
            print(error)
            pass

        try:
            copyfile(write_in, tmp_file)
        except FileNotFoundError:
            print("File not found: {}".format(tmp_file))
            pass
    
        self.writer.write_file(write_in, tmp_file, data, 'a')

        return WRITE_OK

    def requested_replica_write(self, folder_to_write, file_to_write, data):
        write_in = self.folder + "/" + folder_to_write + "/" + file_to_write
        tmp_file = self.folder + "/" + folder_to_write + "/" + TMP_FILE_NAME

        print("Requested replica")

        try:
            os.makedirs(self.folder + "/" + folder_to_write)
            print("Directory created (Didnt exist)")
        except OSError as error:
            print("{} - Replica node".format(error))
            pass

        self.writer.write_file(write_in, tmp_file, data, 'w')

        print("Replicated successfully")

        return WRITE_OK
