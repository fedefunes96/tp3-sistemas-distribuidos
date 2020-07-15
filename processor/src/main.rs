use std::{thread, time};
use std::env;
#[macro_use]
extern crate log;
extern crate simple_logger;
mod protocol;
mod processor;

fn main() {
    load_properties();
    simple_logger::init_with_level(get_log_level_from_env()).unwrap();

    let rabbit_sleep_time = env::var("RABBIT_SLEEP_TIME").unwrap().parse::<u64>().unwrap();
    thread::sleep(time::Duration::from_millis(rabbit_sleep_time*1000));

    let host = env::var("RABBITMQ_ADDR").unwrap();
    let reader_queue = env::var("READER_QUEUE").unwrap();
    let map_queue = env::var("QUEUE_MAP").unwrap();
    let date_queue = env::var("QUEUE_DATE").unwrap();
    let count_queue = env::var("QUEUE_COUNT").unwrap();
    let eof_map_queue = env::var("EOF_MAP").unwrap();
    let eof_date_queue = env::var("EOF_DATE").unwrap();
    let eof_count_queue = env::var("EOF_COUNT").unwrap();
    let topic_places = env::var("TOPIC_PLACES").unwrap();

    let processor = processor::Processor::new(
        host,
        reader_queue,
        map_queue,
        date_queue,
        count_queue,
        eof_map_queue,
        eof_date_queue,
        eof_count_queue,
        topic_places
    );

    processor.connect();
    processor.process_messages();
}

fn load_properties() {
    let properties = dotproperties::parse_from_file("./config/processor-config.properties").unwrap();
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