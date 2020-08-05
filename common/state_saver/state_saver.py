import json
from secure_data.secure_data import SecureData

class StateSaver:
    def __init__(self, stage, cluster_w_dir, cluster_r_dir):
        self.stage = stage
        self.secure_data = SecureData(cluster_w_dir, cluster_r_dir)

    def save_state(self, connection_id, message_id, content):
        folder = connection_id + "/" + self.stage

        data_to_save = []

        response = self.secure_data.read_file(folder, self.stage)

        if response == None or response == "":
            data_to_save = [content, message_id]
        else:
            data_to_save = json.loads(response)
            #Override last content
            data_to_save[0] = content
            #Add new message to duplicate filter
            data_to_save.append(message_id)

        self.secure_data.write_to_file(folder, self.stage, json.dumps(data_to_save))
    
    def is_duplicated(self, connection_id, message_id):
        folder = connection_id + "/" + self.stage

        msg = self.secure_data.read_file(folder, self.stage)

        if msg == None or msg == "":
            return False

        data = json.loads(msg)

        return message_id in data[1:]    

    def load_state(self, connection_id):
        folder = connection_id + "/" + self.stage

        msg = self.secure_data.read_file(folder, self.stage)

        if msg == None or msg == "":
            return None
        
        return json.loads(msg)[0]
