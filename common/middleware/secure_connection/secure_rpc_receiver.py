from middleware.secure_connection.secure_receiver import SecureReceiver

class SecureRpcReceiver(SecureReceiver):
    def create_channel(self):
        return self.connection.create_rpc_receiver(self.queue)
