use amiquip::{Connection, Channel, Queue, QueueDeclareOptions, Exchange, Publish, ExchangeType, ExchangeDeclareOptions};

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
    topic_places: String,
    receiver_queue: String
}

impl Protocol<'static> {

    pub fn new(host: String,
        receiver_queue: String,
        map_queue: String,
        date_queue: String,
        count_queue: String,
        topic_places: String
    ) -> Protocol<'static> {

        Protocol {
            host: host,
            map_queue: map_queue,
            date_queue: date_queue,
            count_queue: count_queue,
            topic_places: topic_places,
            receiver_queue: receiver_queue,
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

    pub fn process_places(&self, region: String, latitude: String, longitude: String) {
        let message = format!("{},{},{}", region, latitude, longitude);

        self.send_places_message(message.as_str());
    }

    pub fn send_no_more_places(&self) {
        self.send_places_message("EOF");
    }

    fn send_places_message(&self, message: &str) {
        match &self.fanout_exchange {
            Some(exchange) => exchange.publish(Publish::new(message.as_bytes(), "")).unwrap(),
            None => {}
        }
    }

    pub fn process_case(&self, date: &str, latitude: &str, longitude: &str, result: &str) {
        self.send_message_to_queue(result, &self.count_queue);
        let date_counter_message = format!("{}{}", if result == "positivi" {"P"} else {"D"}, date);
        self.send_message_to_queue(&date_counter_message, &self.date_queue);
        if result == "positivi" {
            self.send_message_to_queue(&format!("{}//{}", latitude, longitude), &self.map_queue);
        }
    }

    fn send_message_to_queue(&self, message: &str, queue: &str) {
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
            fanout_exchange: None,
            receiver: None,
            map_queue: String::from(""),
            date_queue: String::from(""),
            count_queue: String::from(""),
            host: String::from(""),
            topic_places: String::from(""),
            receiver_queue: String::from("")
        }
    }
}