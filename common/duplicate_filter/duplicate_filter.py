from common.secure_data.secure_data import SecureData


class DuplicateFilter:
    def __init__(self, cluster_w_dir, cluster_r_dir):
        self.secure_data = SecureData(cluster_w_dir, cluster_r_dir)

    def message_exists(self, connection_id, message_id):
        response = self.secure_data.read_file(connection_id, message_id)
        return response is not None or response != ""

    def insert_message(self, connection_id, message_id, content):
        self.secure_data.write_to_file(connection_id, message_id, content)
