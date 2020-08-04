use std::sync::mpsc::Sender;
use amiquip::{Connection, Channel, Queue, QueueDeclareOptions, ConsumerMessage, ConsumerOptions, Exchange, Publish, /*ExchangeType, ExchangeDeclareOptions,*/ AmqpProperties};

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
    receiver_queue: String,
    receiver_places_queue: String
}

impl Protocol {

    pub fn new(host: String,
               receiver_queue: String,
               receiver_places_queue: String,
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
            receiver_places_queue,
            ..Default::default()
        }

    }

    pub fn connect(& mut self) {
        let mut connection = Connection::insecure_open(self.host.as_str()).unwrap();

        self.channel = Some(connection.open_channel(None).unwrap());
        self.connection = Some(connection);
    }

    pub fn process_places(&self, sender: Sender<String>) {
        let options = QueueDeclareOptions {
            durable: true,
            ..QueueDeclareOptions::default()
        };
        let queue = self.channel.as_ref().unwrap().queue_declare(self.receiver_places_queue.as_str(), options).unwrap();
        self.read_from_queue(&queue, sender)
    }

    pub fn process_cases(&self, sender: Sender<String>) {
        let options = QueueDeclareOptions {
            durable: true,
            ..QueueDeclareOptions::default()
        };
        let queue = self.channel.as_ref().unwrap().queue_declare(self.receiver_queue.as_str(), options).unwrap();
        self.read_from_queue(&queue, sender)
    }

    /*pub fn send_no_more_places(&self) {
        self.send_places_message(String::from("EOF"), String::from("EOF"));
    }*/

    pub fn send_stop_places(&self) {
        self.send_places_message(String::from("STOP"), String::from("STOP"));
    }

    pub fn send_places_message(&self, message: String, type_: String) {
        //let exchange = self.channel.as_ref().unwrap().exchange_declare(ExchangeType::Fanout, self.topic_places.as_str(), ExchangeDeclareOptions::default()).unwrap();
        //let properties = AmqpProperties::default().with_type_(type_);
        //exchange.publish(Publish::with_properties(message.as_bytes(), "", properties)).unwrap();
        self.send_message_to_queue(message.clone(), self.topic_places.clone(), type_.clone());
    }

    pub fn send_case_message(&self, message: String, type_: String) {
        self.send_message_to_queue(message.clone(), self.count_queue.clone(), type_.clone());
        self.send_message_to_queue(message.clone(), self.map_queue.clone(), type_.clone());
        self.send_message_to_queue(message.clone(), self.date_queue.clone(), type_.clone());
    }

    pub fn send_no_more_cases(&self, message: String, type_: String) {
        self.send_message_to_queue(message.clone(), self.eof_map_queue.clone(), type_.clone());
        self.send_message_to_queue(message.clone(), self.eof_count_queue.clone(), type_.clone());
        self.send_message_to_queue(message.clone(), self.eof_date_queue.clone(), type_.clone());
    }

    pub fn send_stop_cases(&self) {
        self.send_message_to_queue(String::from("STOP"), self.eof_map_queue.clone(), String::from("STOP"));
        self.send_message_to_queue(String::from("STOP"), self.eof_count_queue.clone(), String::from("STOP"));
        self.send_message_to_queue(String::from("STOP"), self.eof_date_queue.clone(), String::from("STOP"));
    }

    fn send_message_to_queue(&self, message: String, queue: String, type_: String) {
        let exchange = Exchange::direct(self.channel.as_ref().unwrap());
        let properties = AmqpProperties::default().with_type_(type_);
        exchange.publish(Publish::with_properties(message.as_bytes(), queue, properties)).unwrap();
    }

    fn read_from_queue(&self, queue: &Queue, sender: Sender<String>) {
        let consumer = queue.consume(ConsumerOptions::default()).unwrap();
        for (_, message) in consumer.receiver().iter().enumerate() {
            match message {
                ConsumerMessage::Delivery(delivery) => {
                    let body = String::from_utf8_lossy(&delivery.body);
                    sender.send(body.to_string()).unwrap();

                    let msg: Vec<&str> = body.split(',').collect();

                    if body == "STOP" || msg[2] == "EOF" {
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

    pub fn close(&mut self) {
        drop(self.channel.as_ref());
        drop(self.connection.as_ref());
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
            receiver_queue: String::from(""),
            receiver_places_queue: String::from("")
        }
    }
}