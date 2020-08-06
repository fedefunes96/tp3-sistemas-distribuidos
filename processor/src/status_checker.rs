use amiquip::{Connection, Channel, Exchange, Publish, AmqpProperties};
use rand::distributions::{Distribution, Uniform};
use std::thread;
use std::time::Duration;

pub struct StatusChecker {
    connection: Option<Connection>,
    channel: Option<Channel>,
    host: String,
    status_queue: String,
    worker_id: String,
    worker_type: String,
}

impl StatusChecker {
    pub fn new(host: String,
               status_queue: String,
               worker_id: String,
               worker_type: String,
    ) -> StatusChecker {
        StatusChecker {
            host,
            status_queue,
            worker_id,
            worker_type,
            ..Default::default()
    }
        }

    pub fn connect(&mut self) {
        loop {
            match Connection::insecure_open(self.host.as_str()) {
                Ok(conn) => {
                    let mut connection = conn;
                    self.channel.replace(connection.open_channel(None).unwrap());
                    self.connection.replace(connection);
                    break;
                }
                Err(_) => {}
            }
        }
    }

    pub fn start(&mut self) {
        let distribution = Uniform::from(5..15);
        let mut rng = rand::thread_rng();
        loop {
            let time_secs = distribution.sample(&mut rng);
            thread::sleep(Duration::from_secs(time_secs));
            self.send_status();
        }
    }

    fn send_status(&mut self) {
        let message = format!("ALIVE,{},{}", self.worker_id, self.worker_type);
        self.send_message_to_queue(message.clone(), self.status_queue.clone(), String::from("STATUS"));
    }

    fn send_message_to_queue(&mut self, message: String, queue: String, type_: String) {
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

    pub fn close(&mut self) {
        drop(self.channel.as_ref());
        drop(self.connection.as_ref());
    }
}

impl Default for StatusChecker {
    fn default() -> StatusChecker {
        StatusChecker {
            connection: None,
            channel: None,
            status_queue: String::from(""),
            worker_id: String::from(""),
            worker_type: String::from(""),
            host: String::from("")
        }
    }
}
