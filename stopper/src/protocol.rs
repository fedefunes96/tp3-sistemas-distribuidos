use amiquip::{Connection, Channel, Exchange, Publish};

pub struct Protocol {
    connection: Option<Connection>,
    channel: Option<Channel>,
    host: String,
    processor_queue: String,
    processor_places_queue: String
}

impl Protocol {

    pub fn new(host: String,
        processor_queue: String,
        processor_places_queue: String
    ) -> Protocol {

        Protocol {
            host,
            processor_queue,
            processor_places_queue,
            ..Default::default()
        }

    }

    pub fn connect(& mut self) {
        let mut connection = Connection::insecure_open(self.host.as_str()).unwrap();

        self.channel = Some(connection.open_channel(None).unwrap());
        self.connection = Some(connection);
    }

    pub fn stop_places(&self) {
        self.send_message_to_queue(String::from("STOP"), self.processor_places_queue.as_str());
    }

    pub fn stop_cases(&self) {
        self.send_message_to_queue(String::from("STOP"), self.processor_queue.as_str());
        self.send_message_to_queue(String::from("STOP"), self.processor_queue.as_str());
    }

    fn send_message_to_queue(&self, message: String, queue: &str) {
        let exchange = Exchange::direct(self.channel.as_ref().unwrap());
        exchange.publish(Publish::new(message.as_bytes(), queue)).unwrap();
    }

    pub fn close(& mut self) {
        drop(self.channel.as_ref());
        drop(self.connection.as_ref());
    }
}

impl Default for Protocol {
    fn default () -> Protocol {
        Protocol {
            connection: None,
            channel: None,
            host: String::from(""),
            processor_queue: String::from(""),
            processor_places_queue: String::from("")
        }
    }
}