use amiquip::{Connection, Channel, Exchange, Publish, AmqpProperties};
use uuid::Uuid;

pub struct Protocol {
    connection: Option<Connection>,
    channel: Option<Channel>,
    host: String,
    processor_queue: String
}

impl Protocol {

    pub fn new(host: String,
        processor_queue: String
    ) -> Protocol {

        Protocol {
            host,
            processor_queue,
            ..Default::default()
        }

    }

    pub fn connect(& mut self) {
        let mut connection = Connection::insecure_open(self.host.as_str()).unwrap();

        self.channel = Some(connection.open_channel(None).unwrap());
        self.connection = Some(connection);
    }

    pub fn process_place(&self, region: String, latitude: f64, longitude: f64, connection_id: String) {
        let message_id = Uuid::new_v4();
        let message = format!("{},{},{},{},{}", connection_id, message_id, region, latitude, longitude);

        self.send_message_to_queue(message, self.processor_queue.as_str(), String::from("PLACE"));
    }

    pub fn process_case(&self, tipo: String, latitude: f64, longitude: f64, date: String, connection_id: String) {
        let message_id = Uuid::new_v4();
        let message = format!("{},{},{},{},{},{}", connection_id, message_id, date, latitude, longitude, tipo);

        self.send_message_to_queue(message, self.processor_queue.as_str(), String::from("CASE"));
    }

    pub fn send_places_end_of_file(&self, connection_id: String) {
        let message_id = Uuid::new_v4();
        let message = format!("{},{},{}", connection_id, message_id, String::from("EOF"));
        self.send_message_to_queue(message, self.processor_queue.as_str(), String::from("PLACE"));
    }

    pub fn send_cases_end_of_file(&self, connection_id: String) {
        let message_id = Uuid::new_v4();
        let message = format!("{},{},{}", connection_id, message_id, String::from("EOF"));        
        self.send_message_to_queue(message, self.processor_queue.as_str(), String::from("CASE"));
    }

    fn send_message_to_queue(&self, message: String, queue: &str, type_: String) {
        let properties = AmqpProperties::default().with_type_(type_);
        let exchange = Exchange::direct(self.channel.as_ref().unwrap());
        exchange.publish(Publish::with_properties(message.clone().as_bytes(), queue.clone(), properties.clone())).unwrap();
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
            processor_queue: String::from("")
        }
    }
}