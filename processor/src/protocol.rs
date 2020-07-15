use std::sync::mpsc::Sender;
use amiquip::{Connection, Channel, Queue, QueueDeclareOptions, ConsumerMessage, ConsumerOptions, Exchange, Publish, ExchangeType, ExchangeDeclareOptions};

pub struct Protocol<'a> {
    connection: Option<Connection>,
    channel: Option<Channel>,
    direct_exchange: Option<Exchange<'a>>,
    fanout_exchange: Option<Exchange<'a>>,
    receiver: Option<Queue<'a>>,
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

impl Protocol<'static> {

    pub fn new(host: String,
               receiver_queue: String,
               map_queue: String,
               date_queue: String,
               count_queue: String,
               eof_map_queue: String,
               eof_date_queue: String,
               eof_count_queue: String,
               topic_places: String
    ) -> Protocol<'static> {

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

    pub fn connect(&'static mut self) {
        let mut connection = Connection::insecure_open(self.host.as_str()).unwrap();

        self.channel = Some(connection.open_channel(None).unwrap());
        self.connection = Some(connection);

        self.direct_exchange = Some(Exchange::direct(self.channel.as_ref().unwrap()));
        self.fanout_exchange = Some(self.channel.as_ref().unwrap().exchange_declare(ExchangeType::Fanout, self.topic_places.as_str(), ExchangeDeclareOptions::default()).unwrap());
        self.receiver = Some(self.channel.as_ref().unwrap().queue_declare(self.receiver_queue.as_str(), QueueDeclareOptions::default()).unwrap());
    }

    pub fn process_places(&self, sender: Sender<String>) {
        match &self.receiver {
            Some(queue) => { self.read_from_queue(queue, sender) },
            None => {}
        }
    }

    pub fn send_no_more_places(&self) {
        self.send_places_message(String::from("EOF"));
    }

    pub fn send_places_message(&self, message: String) {
        match &self.fanout_exchange {
            Some(exchange) => exchange.publish(Publish::new(message.as_bytes(), "")).unwrap(),
            None => {}
        }
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
        match &self.direct_exchange {
            Some(exchange) => exchange.publish(Publish::new(message.as_bytes(), queue)).unwrap(),
            None => {}
        }
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

impl Default for Protocol<'static> {
    fn default () -> Protocol<'static> {
        Protocol {
            connection: None,
            channel: None,
            direct_exchange: None,
            fanout_exchange: None,
            receiver: None,
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