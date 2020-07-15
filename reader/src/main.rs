use std::{thread, time};
use std::env;
mod reader;
mod case;
mod protocol;
mod region;
#[macro_use]
extern crate log;
extern crate simple_logger;

fn main() {
    load_properties();
    simple_logger::init_with_level(get_log_level_from_env()).unwrap();

    let rabbit_sleep_time = env::var("RABBIT_SLEEP_TIME").unwrap().parse::<u64>().unwrap();
    thread::sleep(time::Duration::from_millis(rabbit_sleep_time*1000));

    let processor_quantity = env::var("PROCESSOR_QUANTITY").unwrap().parse::<u32>().unwrap();
    let processor_queue = env::var("PROCESSOR_QUEUE").unwrap();
    let host = env::var("RABBITMQ_ADDR").unwrap();
    let reader = reader::Reader::new(host, processor_queue, processor_quantity);
    reader.connect();
    info!("Connected ro Rabbit!");

    reader.process_places("data/places.csv");
    info!("Finished processing regions");
    reader.process_cases("data/data.csv");
    info!("Finished processing data");
}

fn load_properties() {
    let properties = dotproperties::parse_from_file("./config/reader-config.properties").unwrap();
    for (key, value) in properties {
        env::set_var(key, value);
    }
}

fn get_log_level_from_env() -> log::Level {
    let level = env::var("LOG_LEVEL").unwrap();
    match level.as_str() {
        "ERROR" => {return log::Level::Error},
        "INFO" => {return log::Level::Info},
        "DEBUG" => {return log::Level::Debug},
        "TRACE" => {return log::Level::Trace},
        _ =>  {return log::Level::Info}
    }
}