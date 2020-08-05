use std::sync::mpsc::channel;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
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
                receiver_queue,
                map_queue,
                date_queue,
                count_queue,
                eof_map_queue,
                eof_date_queue,
                eof_count_queue,
                topic_places
            )
        }
    }

    pub fn connect(&mut self) {
        self.protocol.connect();
    }

    /*pub fn process_places(&mut self, should_stop: Arc<AtomicBool>) {
        let (sender, receiver) = channel();
        self.protocol.process_places(sender);
        for message in receiver.iter() {
            if !self.process_place(message.clone()) {
                should_stop.store(true, Ordering::Relaxed);
                break;
            }
        }
        info!("Finished processing regions");
    }*/

    pub fn process_cases(&mut self, should_stop: Arc<AtomicBool>) {
        let (sender, receiver) = channel();
        self.protocol.process_cases(sender);
        for (message, type_) in receiver.iter() {
            if !self.process(message.clone(), type_) {
                should_stop.store(true, Ordering::Relaxed);
                break;
            }
        }
        info!("Finished processing messages");
    }

    fn process(& mut self, body: String, type_: String) -> bool {
        return match type_.as_str() {
            "PLACE" => { self.process_place(body) }
            "CASE" => { self.process_case(body) }
            _ => { true }
        }
    }

    fn process_place(& mut self, body: String) -> bool {
        if body == "STOP" {
            self.protocol.send_stop_places();
            return false;
        }

        let msg: Vec<&str> = body.split(',').collect();

        if msg[2] == "EOF" {
            self.protocol.send_places_message(body.clone(), String::from("EOF"));
        } else {
            self.protocol.send_places_message(body.clone(), String::from("NORMAL"));
        }
        return true;
    }

    fn process_case(& mut self, body: String) -> bool {
        if body == "STOP" {
            self.protocol.send_stop_cases();
            return false;
        }

        let msg: Vec<&str> = body.split(',').collect();

        if msg[2] == "EOF" {
            self.protocol.send_no_more_cases(body.clone(), String::from("EOF"));
        } else {
            self.protocol.send_case_message(body.clone(), String::from("NORMAL"));
        }
        return true;
    }
}

impl Drop for Processor {
    fn drop(&mut self) {
        self.protocol.close();
    }
}