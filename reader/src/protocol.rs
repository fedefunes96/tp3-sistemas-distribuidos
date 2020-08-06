use amiquip::{Connection, Channel, Exchange, Publish, AmqpProperties, QueueDeclareOptions, ConsumerOptions, ConsumerMessage};
use uuid::Uuid;
use std::sync::atomic::{AtomicBool, Ordering};

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

    pub fn can_process(&self, coordinator_queue: String, message: String) -> bool {
        let corr_id = Uuid::new_v4().to_string();
        let reply_to = String::from("client_coordination_queue");
        self.send_rpc_message_to_queue(message, &coordinator_queue, String::from("NEW_CLIENT"), reply_to.clone(), corr_id);
        return self.read_one_message_from_queue(reply_to);
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

    fn send_rpc_message_to_queue(&self, message: String, queue: &str, type_: String, reply_to: String, corr_id: String) {
        let properties = AmqpProperties::default().with_type_(type_).with_correlation_id(corr_id).with_reply_to(reply_to);
        let exchange = Exchange::direct(self.channel.as_ref().unwrap());
        exchange.publish(Publish::with_properties(message.clone().as_bytes(), queue.clone(), properties.clone())).unwrap();
    }

    fn read_one_message_from_queue(&self, queue: String) -> bool {
        let options = QueueDeclareOptions {
            durable: true,
            ..QueueDeclareOptions::default()
        };
        let response = AtomicBool::new(true);
        let queue = self.channel.as_ref().unwrap().queue_declare(queue.as_str(), options).unwrap();
        let consumer = queue.consume(ConsumerOptions::default()).unwrap();
        for (_, message) in consumer.receiver().iter().enumerate() {
            match message {
                ConsumerMessage::Delivery(delivery) => {
                    let body = String::from_utf8_lossy(&delivery.body);
                    info!("Got message!");
                    if body == "READY" {
                        response.store(true, Ordering::Relaxed);
                    } else {
                        response.store(false, Ordering::Relaxed);
                    }
                    consumer.ack(delivery).unwrap();
                    break;
                }
                _ => {
                    break;
                }
            }
        }
        return response.load(Ordering::Relaxed);
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