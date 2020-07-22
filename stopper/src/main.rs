use std::env;
mod stopper;
mod protocol;
#[macro_use]
extern crate log;
extern crate simple_logger;

fn main() {
    simple_logger::init_with_level(get_log_level_from_env()).unwrap();

    let processor_quantity = env::var("PROCESSOR_QUANTITY").unwrap().parse::<u32>().unwrap();
    let processor_queue = env::var("PROCESSOR_QUEUE").unwrap();
    let processor_places_queue = env::var("PROCESSOR_PLACES_QUEUE").unwrap();
    let host = env::var("RABBITMQ_ADDR").unwrap();
    let mut stopper = stopper::Stopper::new(host, processor_queue, processor_places_queue, processor_quantity);
    stopper.connect();
    info!("Connected ro Rabbit!");

    stopper.stop();
    info!("Finished stopping processors");
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