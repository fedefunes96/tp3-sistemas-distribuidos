use std::sync::mpsc::Sender;
use amiquip::{Connection, Channel, QueueDeclareOptions, ConsumerMessage, ConsumerOptions, Exchange, Publish, AmqpProperties};

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
        loop {
            match Connection::insecure_open(self.host.as_str()) {
                Ok(conn) => {
                    let mut connection = conn;
                    self.channel.replace(connection.open_channel(None).unwrap());
                    self.connection.replace(connection);
                    break;
                },
                Err(_) => {}
            }
        }
    }

    pub fn process_cases(& mut self, sender: Sender<(String, String)>) {
        self.read_from_queue(self.receiver_queue.clone(), sender)
    }

    pub fn send_stop_places(& mut self) {
        self.send_places_message(String::from("STOP"), String::from("STOP"));
    }

    pub fn send_places_message(& mut self, message: String, type_: String) {
        self.send_message_to_queue(message.clone(), self.topic_places.clone(), type_.clone());
    }

    pub fn send_case_message(& mut self, message: String, type_: String) {
        self.send_message_to_queue(message.clone(), self.count_queue.clone(), type_.clone());
        self.send_message_to_queue(message.clone(), self.map_queue.clone(), type_.clone());
        self.send_message_to_queue(message.clone(), self.date_queue.clone(), type_.clone());
    }

    pub fn send_no_more_cases(& mut self, message: String, type_: String) {
        self.send_message_to_queue(message.clone(), self.eof_map_queue.clone(), type_.clone());
        self.send_message_to_queue(message.clone(), self.eof_count_queue.clone(), type_.clone());
        self.send_message_to_queue(message.clone(), self.eof_date_queue.clone(), type_.clone());
    }

    pub fn send_stop_cases(& mut self) {
        self.send_message_to_queue(String::from("STOP"), self.eof_map_queue.clone(), String::from("STOP"));
        self.send_message_to_queue(String::from("STOP"), self.eof_count_queue.clone(), String::from("STOP"));
        self.send_message_to_queue(String::from("STOP"), self.eof_date_queue.clone(), String::from("STOP"));
    }

    fn send_message_to_queue(& mut self, message: String, queue: String, type_: String) {
        let channel_taken = self.channel.take();
        let channel = channel_taken.unwrap();
        let exchange = Exchange::direct(&channel);
        let properties = AmqpProperties::default().with_type_(type_);
        loop {
            match exchange.publish(Publish::with_properties(message.clone().as_bytes(), queue.clone(), properties.clone())) {
                Ok(()) => break,
                Err(_) => self.connect()
            }
        }
        self.channel.replace(channel);
    }

    fn read_from_queue(&self, queue: String, sender: Sender<(String, String)>) {
        let options = QueueDeclareOptions {
            durable: true,
            ..QueueDeclareOptions::default()
        };
        let queue = self.channel.as_ref().unwrap().queue_declare(queue.as_str(), options).unwrap();
        let consumer = queue.consume(ConsumerOptions::default()).unwrap();
        for (_, message) in consumer.receiver().iter().enumerate() {
            match message {
                ConsumerMessage::Delivery(delivery) => {
                    let body = String::from_utf8_lossy(&delivery.body);
                    let type_ = delivery.properties.type_().as_ref().unwrap();
                    sender.send((body.to_string(), type_.to_string())).unwrap();

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
            receiver_queue: String::from("")
        }
    }
}