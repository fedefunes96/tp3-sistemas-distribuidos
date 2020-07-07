use amiquip::{Connection, Channel, Queue, QueueDeclareOptions, Exchange, Publish, ExchangeType, ExchangeDeclareOptions};

pub struct Protocol<'a> {
    connection: Connection,
    channel: Channel,
    direct_exchange: Exchange<'a>,
    fanout_exchange: Exchange<'a>,
    receiver: Queue<'a>,
    map_queue: &'a str,
    date_queue: &'a str,
    count_queue: &'a str
}

impl Protocol<'static> {

    pub fn new(host: &str,
        receiver_queue: &str,
        map_queue: &'static str,
        date_queue: &'static str,
        count_queue: &'static str,
        topic_places: &'static str
    ) -> Protocol<'static> {

        let mut connection = Connection::insecure_open(host).unwrap();
        let channel = connection.open_channel(None).unwrap();
        let direct_exchange = Exchange::direct(&channel);
        let fanout_exchange = channel.copy().exchange_declare(ExchangeType::Fanout, topic_places, ExchangeDeclareOptions::default()).unwrap();
        let receiver = channel.queue_declare(receiver_queue, QueueDeclareOptions::default()).unwrap();

        Protocol {
            connection,
            channel,
            direct_exchange,
            fanout_exchange,
            receiver,
            map_queue,
            date_queue,
            count_queue
        }

    }

    pub fn process_places(&self, region: String, latitude: String, longitude: String) {
        let message = format!("{},{},{}", region, latitude, longitude);

        self.fanout_exchange.publish(Publish::new(message.as_bytes(), "")).unwrap();
    }

}