use amiquip::{Connection, Channel, Exchange, Publish};

pub struct Protocol<'a> {
    connection: Option<Connection>,
    channel: Option<Channel>,
    direct_exchange: Option<Exchange<'a>>,
    host: String,
    processor_queue: String
}

impl Protocol<'static> {

    pub fn new(host: String,
        processor_queue: String
    ) -> Protocol<'static> {

        Protocol {
            host,
            processor_queue,
            ..Default::default()
        }

    }

    pub fn connect(&'static mut self) {
        let mut connection = Connection::insecure_open(self.host.as_str()).unwrap();

        self.channel = Some(connection.open_channel(None).unwrap());
        self.connection = Some(connection);

        self.direct_exchange = Some(Exchange::direct(self.channel.as_ref().unwrap()));
    }

    pub fn process_place(&self, region: String, latitude: f64, longitude: f64) {
        let message = format!("{},{},{}", region, latitude, longitude);

        self.send_message_to_queue(message, self.processor_queue.as_str());
    }

    pub fn process_case(&self, tipo: String, latitude: f64, longitude: f64, date: String) {
        let message = format!("{},{},{},{}", date, latitude, longitude, tipo);

        self.send_message_to_queue(message, self.processor_queue.as_str());
    }

    pub fn send_end_of_file(&self) {
        self.send_message_to_queue(String::from("EOF"), self.processor_queue.as_str());
    }

    fn send_message_to_queue(&self, message: String, queue: &str) {
        match &self.direct_exchange {
            Some(exchange) => exchange.publish(Publish::new(message.as_bytes(), queue)).unwrap(),
            None => {}
        }
    }

}

impl Default for Protocol<'static> {
    fn default () -> Protocol<'static> {
        Protocol {
            connection: None,
            channel: None,
            direct_exchange: None,
            host: String::from(""),
            processor_queue: String::from("")
        }
    }
}

impl Drop for Protocol {
    fn drop(& mut self) {
        drop(self.direct_exchange);
        drop(self.channel);
        drop(self.connection);
    }
}