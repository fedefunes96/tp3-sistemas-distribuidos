from middleware.secure_connection.secure_receiver import SecureReceiver

class SecureRpcReceiver(SecureReceiver):
    def create_channel(self):
        return self.connection.create_rpc_receiver(self.queue)

    def reply(self, cor_id, reply_to, msg):
        tries_before_giving_up = 2

        while tries_before_giving_up > 0:
            try:
                self.receiver.reply(cor_id, reply_to, msg)
            except:
                self.connection.force_connect()
            finally:
                tries_before_giving_up -= 1

    #def start_receiving(self, data_read):
    #    self.receiver = self.create_channel()
    #    self.receiver.start_receiving(data_read)

    def restart_queue(self):
        self.receiver.restart_queue()