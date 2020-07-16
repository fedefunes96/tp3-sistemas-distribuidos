use std::sync::mpsc::Sender;
use amiquip::{Connection, Channel, Queue, QueueDeclareOptions, ConsumerMessage, ConsumerOptions, Exchange, Publish, ExchangeType, ExchangeDeclareOptions};

pub struct Protocol {
    connection: Option<Connection>,
    channel: Option<Channel>,
    host: String,
    map_queue: String,
    date_queue: String,
    count_queue: String,
    eof_map_queue: String,
    eof_date_queue: String,
    eof_count_queue: String,
    topic_places: String,
    receiver_queue: String
}

impl Protocol {

    pub fn new(host: String,
               receiver_queue: String,
               map_queue: String,
               date_queue: String,
               count_queue: String,
               eof_map_queue: String,
               eof_date_queue: String,
               eof_count_queue: String,
               topic_places: String
    ) -> Protocol {

        Protocol {
            host,
            map_queue,
            date_queue,
            count_queue,
            eof_map_queue,
            eof_date_queue,
            eof_count_queue,
            topic_places,
            receiver_queue,
            ..Default::default()
        }

    }

    pub fn connect(& mut self) {
        let mut connection = Connection::insecure_open(self.host.as_str()).unwrap();

        self.channel = Some(connection.open_channel(None).unwrap());
        self.connection = Some(connection);
    }

    pub fn process_places(&self, sender: Sender<String>) {
        let queue = self.channel.as_ref().unwrap().queue_declare(self.receiver_queue.as_str(), QueueDeclareOptions::default()).unwrap();
        self.read_from_queue(&queue, sender)
    }

    pub fn send_no_more_places(&self) {
        self.send_places_message(String::from("EOF"));
    }

    pub fn send_places_message(&self, message: String) {
        let exchange = self.channel.as_ref().unwrap().exchange_declare(ExchangeType::Fanout, self.topic_places.as_str(), ExchangeDeclareOptions::default()).unwrap();
        exchange.publish(Publish::new(message.as_bytes(), "")).unwrap();
    }

    pub fn send_case_message(&self, message: String) {
        self.send_message_to_queue(message.clone(), self.count_queue.clone());
        self.send_message_to_queue(message.clone(), self.map_queue.clone());
        self.send_message_to_queue(message.clone(), self.date_queue.clone());
    }

    pub fn send_no_more_cases(&self) {
        self.send_message_to_queue(String::from("EOF"), self.eof_map_queue.clone());
        self.send_message_to_queue(String::from("EOF"), self.eof_count_queue.clone());
        self.send_message_to_queue(String::from("EOF"), self.eof_date_queue.clone());
    }

    fn send_message_to_queue(&self, message: String, queue: String) {
        let exchange = Exchange::direct(self.channel.as_ref().unwrap());
        exchange.publish(Publish::new(message.as_bytes(), queue)).unwrap();
    }

    fn read_from_queue(&self, queue: &Queue, sender: Sender<String>) {
        let consumer = queue.consume(ConsumerOptions::default()).unwrap();
        for (_, message) in consumer.receiver().iter().enumerate() {
            match message {
                ConsumerMessage::Delivery(delivery) => {
                    let body = String::from_utf8_lossy(&delivery.body);
                    sender.send(body.to_string()).unwrap();
                    if body == "EOF" {
                        consumer.ack(delivery).unwrap();
                        break;
                    }
                    consumer.ack(delivery).unwrap();
                }
                other => {
                    info!("Consumer ended: {:?}", other);
                    break;
                }
            }
        }
    }

}

impl Default for Protocol {
    fn default () -> Protocol {
        Protocol {
            connection: None,
            channel: None,
            map_queue: String::from(""),
            date_queue: String::from(""),
            count_queue: String::from(""),
            eof_map_queue: String::from(""),
            eof_date_queue: String::from(""),
            eof_count_queue: String::from(""),
            host: String::from(""),
            topic_places: String::from(""),
            receiver_queue: String::from("")
        }
    }
}