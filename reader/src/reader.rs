use std::fs::File;
use std::io::prelude::*;
use crate::protocol::Protocol;
use crate::region::Region;
use crate::case::Case;

pub struct Reader {
    protocol: Protocol,
    processor_quantity: u32
}

impl Reader {

    pub fn new(host: String,
        processor_queue: String,
        processor_quantity: u32) -> Reader {
        Reader { protocol: Protocol::new(host, processor_queue), processor_quantity }
    }

    pub fn connect(&mut self) {
        self.protocol.connect();
    }

    pub fn can_process(&mut self, coordinator_queue: String, connection_id: String) -> bool {
        let message = format!("[\"{}\",\"NEW_CLIENT\"]", connection_id);
        return self.protocol.can_process(coordinator_queue, message);

    }

    pub fn process_places(&self, route: &str, connection_id: String) {
        let mut file = File::open(route).unwrap();
        let mut contents = String::new();
        file.read_to_string(&mut contents).unwrap();
        let mut reader = csv::Reader::from_reader(contents.as_bytes());
        for record in reader.deserialize() {
            let record: Region = record.unwrap();
            info!("[{}] {}: ({}, {})", connection_id.clone(), record.denominazione_regione, record.lat, record.long);
            self.protocol.process_place(record.denominazione_regione, record.lat, record.long, connection_id.clone());
        }
        info!("Finished processing regions");
        for _ in 0..self.processor_quantity {
            self.protocol.send_places_end_of_file(connection_id.clone());
        }
        info!("Finished sending EOFs");
    }

    pub fn process_cases(&self, route: &str, connection_id: String) {
        let mut cases_file = File::open(route).unwrap();
        let mut cases_contents = String::new();
        cases_file.read_to_string(&mut cases_contents).unwrap();
        let mut cases_reader = csv::Reader::from_reader(cases_contents.as_bytes());
        for record in cases_reader.deserialize() {
            let record: Case = record.unwrap();
            self.protocol.process_case(record.tipo, record.lat, record.long, record.data, connection_id.clone());
        }
        info!("Finished processing cases");
        for _ in 0..self.processor_quantity {
            self.protocol.send_cases_end_of_file(connection_id.clone());
        }
        info!("Finished sending EOFs");
    }
}

impl Drop for Reader {
    fn drop(&mut self) {
        self.protocol.close();
    }
}
