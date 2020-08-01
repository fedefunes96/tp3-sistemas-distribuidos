from middleware.secure_connection.secure_sender import SecureSender

class SecureRpcSender(SecureSender):
    def create_channel(self):
        return self.connection.create_rpc_sender(self.queue)

    def send(self, msg, timeout=None):
        while True:
            try:
                self.sender = self.create_channel()
                return self.sender.send(msg, timeout)
            except:
                print("RPC Send raised exception")
                self.connection.force_connect()
