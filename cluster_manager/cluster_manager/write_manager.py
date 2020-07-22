import os
from shutil import copyfile

TMP_FILE_NAME = "tmp.txt"

class WriteManager:
    def __init__(self, folder, recv_queue, replicas_queues):
        self.folder = folder
        self.protocol = WriteProtocol(recv_queue, replicas_queues)
        
    def start(self):
        self.protocol.start_receiving(self.requested_write)
    
    def requested_write(self, folder_to_write, file_to_write, data):
        write_in = self.folder + "/" + folder_to_write + "/" + file_to_write
        tmp_file = self.folder + "/" + folder_to_write + "/" + TMP_FILE_NAME

        #Only one write request
        self.write_file(write_in, tmp_file, data, 'w')
        self.protocol.replicate_data()

    def requested_append(self, folder_to_write, file_to_write, data):
        write_in = self.folder + "/" + folder_to_write + "/" + file_to_write
        tmp_file = self.folder + "/" + folder_to_write + "/" + TMP_FILE_NAME

        try:
            copyfile(write_in, tmp_file)
        except FileNotFoundError:
            pass

        self.write_file(write_in, tmp_file, 'a')           

    def requested_replica(self, folder_to_write, file_to_write, data):
        self.requested_write(folder_to_write, file_to_write, data)

    def write_file(self, write_in, tmp_file, data, mode):
        #Writes file 'write_in' with 'data' using a temp file passed
        f = open(tmp_file, mode)
        f.write(data)
        f.flush()
        os.fsync(f.fileno()) 
        f.close()

        #Is atomic
        os.rename(tmp_file, write_in)
