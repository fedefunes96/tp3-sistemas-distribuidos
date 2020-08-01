from middleware.secure_connection.secure_receiver import SecureReceiver

class SecureDistributedReceiver(SecureReceiver):
    def create_channel(self):
        return self.connection.create_distributed_work_receiver(self.queue)
