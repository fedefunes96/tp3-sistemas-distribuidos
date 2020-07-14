use amiquip::{Connection, Channel, Queue, QueueDeclareOptions, Exchange, Publish, ExchangeType, ExchangeDeclareOptions};

pub struct Processor {

}

impl Processor {

    pub fn new() -> Processor {
        Processor {}
    }

    pub fn process_places(&self) {

    }

    pub fn process_cases(&self) {

    }
}

impl Default for Processor {
    fn default () -> Processor {
        Processor {}
    }
}