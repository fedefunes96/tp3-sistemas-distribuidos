import os

class Writer:
    def write_file(self, write_in, tmp_file, data, mode):
        print("Going to write: " + data + " in file:" + write_in)
        #Writes file 'write_in' with 'data' using a temp file passed
        f = open(tmp_file, mode)
        f.write(data)
        f.flush()
        os.fsync(f.fileno()) 
        f.close()

        #Is atomic
        os.rename(tmp_file, write_in)
