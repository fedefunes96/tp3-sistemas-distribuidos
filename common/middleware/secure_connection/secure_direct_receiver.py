from middleware.secure_connection.secure_receiver import SecureReceiver

class SecureDirectReceiver(SecureReceiver):
    def create_channel(self):
        return self.connection.create_direct_receiver(self.queue)
