from middleware.secure_connection.secure_sender import SecureSender

class SecureRpcSender(SecureSender):
    def create_channel(self):
        return self.connection.create_rpc_sender(self.queue)
