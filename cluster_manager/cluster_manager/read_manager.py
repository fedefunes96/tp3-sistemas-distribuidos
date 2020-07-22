from protocol.read_protocol import ReadProtocol

class ReadManager:
    def __init__(self, folder, recv_queue):
        self.folder = folder
        self.protocol = ReadProtocol(recv_queue)
        
    def start(self):
        self.protocol.start_receiving(self.requested_read)
    
    def requested_read(self, folder_to_read, file_to_read):
        read_in = self.folder + "/" + folder_to_read + "/" + file_to_read

        #If a write overwrites this file, i'll read last content
        #as the file is replaced but i have an open file descriptor
        content = ''

        try:
            f = open(read_in, 'r')
            content = f.read()
            f.close()
        except FileNotFoundError:
            pass

        return content
