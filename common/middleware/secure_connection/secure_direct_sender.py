from middleware.secure_connection.secure_sender import SecureSender

class SecureDirectSender(SecureSender):
    def create_channel(self):
        return self.connection.create_direct_sender(self.queue)
