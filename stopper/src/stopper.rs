use crate::protocol::Protocol;

pub struct Stopper {
    protocol: Protocol,
    processor_quantity: u32
}

impl Stopper {

    pub fn new(host: String,
        processor_queue: String,
        processor_places_queue: String,
        processor_quantity: u32) -> Stopper {
        Stopper { protocol: Protocol::new(host, processor_queue, processor_places_queue), processor_quantity }
    }

    pub fn connect(&mut self) {
        self.protocol.connect();
    }

    pub fn stop(&self) {
        info!("Finished processing regions");
        for _ in 0..self.processor_quantity {
            self.protocol.stop_places();
            self.protocol.stop_cases();
        }
        info!("Finished sending STOPs");
    }
}

impl Drop for Stopper {
    fn drop(&mut self) {
        self.protocol.close();
    }
}
