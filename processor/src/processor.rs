use std::sync::mpsc::channel;
use crate::protocol::Protocol;

pub struct Processor {
    protocol: Protocol
}

impl Processor {

    pub fn new(host: String,
        receiver_queue: String,
        map_queue: String,
        date_queue: String,
        count_queue: String,
        eof_map_queue: String,
        eof_date_queue: String,
        eof_count_queue: String,
        topic_places: String) -> Processor {
        Processor {
            protocol: Protocol::new(
                host,
                map_queue,
                date_queue,
                count_queue,
                eof_map_queue,
                eof_date_queue,
                eof_count_queue,
                topic_places,
                receiver_queue
            )
        }
    }

    pub fn connect(& mut self) {
        self.protocol.connect();
    }

    pub fn process_messages(&mut self) {
        let (sender, receiver) = channel();
        self.protocol.process_places(sender);
        for message in receiver.iter() {
            self.process_place(message.clone());
            if message == "EOF" {
                self.protocol.send_no_more_places();
                break;
            }
        }
        info!("Finished processing regions");
        for message in receiver.iter() {
            self.process_case(message.clone());
            if message == "EOF" {
                self.protocol.send_no_more_cases();
            }
        }
        info!("Finished processing cases");
    }

    fn process_place(&self, body: String) {
        info!("Got region: {}", body);
        self.protocol.send_places_message(body.clone());
    }

    fn process_case(&self, body: String) {
        self.protocol.send_case_message(body.clone());
    }
}

impl Drop for Processor {
    fn drop(&mut self) {
        self.protocol.close();
    }
}