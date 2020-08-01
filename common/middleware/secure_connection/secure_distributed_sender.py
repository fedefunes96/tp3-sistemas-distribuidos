from middleware.secure_connection.secure_sender import SecureSender

class SecureDistributedSender(SecureSender):
    def create_channel(self):
        return self.connection.create_distributed_work_sender(self.queue)
