use std::env;
use std::{thread, time};
use uuid::Uuid;
mod reader;
mod case;
mod protocol;
mod region;
#[macro_use]
extern crate log;
extern crate simple_logger;

fn main() {
    simple_logger::init_with_level(get_log_level_from_env()).unwrap();

    let processor_quantity = env::var("PROCESSOR_QUANTITY").unwrap().parse::<u32>().unwrap();
    let processor_queue = env::var("PROCESSOR_QUEUE").unwrap();
    let coordinator_queue = env::var("COORDINATOR_QUEUE").unwrap();
    let host = env::var("RABBITMQ_ADDR").unwrap();
    let mut reader = reader::Reader::new(host, processor_queue, processor_quantity);
    reader.connect();
    info!("Connected ro Rabbit!");
    let connection_id = Uuid::new_v4().to_string();

    if !reader.can_process(coordinator_queue, connection_id.clone()) {
        info!("Cannot start. Service is busy.");
        return;
    }
    info!("Got accepted into the service");

    reader.process_places("data/places.csv", connection_id.clone());
    info!("Finished processing regions");
    thread::sleep(time::Duration::from_millis(2*1000));
    reader.process_cases("data/data.csv", connection_id.clone());
    thread::sleep(time::Duration::from_millis(10*1000));
    info!("Finished processing data");
}

fn get_log_level_from_env() -> log::Level {
    let level = env::var("LOG_LEVEL").unwrap();
    return match level.as_str() {
        "ERROR" => { log::Level::Error },
        "INFO" => { log::Level::Info },
        "DEBUG" => { log::Level::Debug },
        "TRACE" => { log::Level::Trace },
        _ => { log::Level::Info }
    }
}