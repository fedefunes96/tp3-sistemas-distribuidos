use std::fs::File;
use std::io::prelude::*;
use crate::protocol::Protocol;
use crate::region::Region;
use crate::case::Case;

pub struct Reader {
    protocol: Protocol<'static>,
    processor_quantity: u32
}

impl Reader {

    pub fn new(host: String,
        processor_queue: String,
        processor_quantity: u32) -> Reader {
        Reader { protocol: Protocol::new(host, processor_queue), processor_quantity }
    }

    pub fn connect(&self) {
        self.protocol.connect();
    }

    pub fn process_places(&self, route: &str) {
        let mut file = File::open(route).unwrap();
        let mut contents = String::new();
        file.read_to_string(&mut contents).unwrap();
        let mut reader = csv::Reader::from_reader(contents.as_bytes());
        for record in reader.deserialize() {
            let record: Region = record.unwrap();
            info!("{}: ({}, {})", record.denominazione_regione, record.lat, record.long);
            self.protocol.process_place(record.denominazione_regione, record.lat, record.long);
        }
        info!("Finished processing regions");
        for _ in 0..self.processor_quantity {
            self.protocol.send_end_of_file();
        }
        info!("Finished sending EOFs");
    }

    pub fn process_cases(&self, route: &str) {
        let mut cases_file = File::open(route).unwrap();
        let mut cases_contents = String::new();
        cases_file.read_to_string(&mut cases_contents).unwrap();
        let mut cases_reader = csv::Reader::from_reader(cases_contents.as_bytes());
        for record in cases_reader.deserialize() {
            let record: Case = record.unwrap();
            self.protocol.process_case(record.tipo, record.lat, record.long, record.data);
        }
        info!("Finished processing cases");
        for _ in 0..self.processor_quantity {
            self.protocol.send_end_of_file();
        }
        info!("Finished sending EOFs");
    }
}

impl Drop for Reader {
    fn drop(&mut self) {
        drop(self.protocol);
    }
}
