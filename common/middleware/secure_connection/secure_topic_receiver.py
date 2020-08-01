from middleware.secure_connection.secure_receiver import SecureReceiver

class SecureTopicReceiver(SecureReceiver):
    def create_channel(self):
        return self.connection.create_topic_receiver(self.queue)