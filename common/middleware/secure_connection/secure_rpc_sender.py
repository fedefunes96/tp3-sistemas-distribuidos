from middleware.exceptions.rpc_timeout import RPCTimeout

class SecureRpcSender:
    def __init__(self, queue, connection):
        self.queue = queue
        self.connection = connection
        self.sender = self.create_channel()

    def create_channel(self):
        return self.connection.create_rpc_sender(self.queue)

    def send(self, msg, timeout=20):
        while True:
            try:
                return self.sender.send(msg, timeout)
            except RPCTimeout as e:
                print("Rpc Timeout, try again")
                continue
            except Exception as e:
                print(e)
                print("RPC Send raised exception")
                self.connection.force_connect()
                self.sender = self.create_channel()
