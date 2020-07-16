use std::env;
#[macro_use]
extern crate log;
extern crate simple_logger;
mod protocol;
mod processor;

fn main() {
    simple_logger::init_with_level(get_log_level_from_env()).unwrap();

    let host = env::var("RABBITMQ_ADDR").unwrap();
    let reader_queue = env::var("READER_QUEUE").unwrap();
    let map_queue = env::var("QUEUE_MAP").unwrap();
    let date_queue = env::var("QUEUE_DATE").unwrap();
    let count_queue = env::var("QUEUE_COUNT").unwrap();
    let eof_map_queue = env::var("EOF_MAP").unwrap();
    let eof_date_queue = env::var("EOF_DATE").unwrap();
    let eof_count_queue = env::var("EOF_COUNT").unwrap();
    let topic_places = env::var("TOPIC_PLACES").unwrap();

    let mut processor = processor::Processor::new(
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