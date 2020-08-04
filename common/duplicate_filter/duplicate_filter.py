from secure_data.secure_data import SecureData


class DuplicateFilter:
    def __init__(self, cluster_w_dir, cluster_r_dir):
        self.secure_data = SecureData(cluster_w_dir, cluster_r_dir)

    def message_exists(self, connection_id, stage, message_id):
        folder = connection_id + "/" + stage
        response = self.secure_data.read_file(folder, message_id)
        return response is not None and response != ""

    def insert_message(self, connection_id, stage, message_id, content):
        folder = connection_id + "/" + stage
        self.secure_data.write_to_file(folder, message_id, content)
