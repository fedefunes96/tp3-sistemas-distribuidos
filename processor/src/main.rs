use std::{thread, time};
use std::env;
use amiquip::{Connection, ConsumerMessage, ConsumerOptions, QueueDeclareOptions, Exchange, Publish, ExchangeType, ExchangeDeclareOptions};
#[macro_use]
extern crate log;
extern crate simple_logger;
mod protocol;


fn main() {
    load_properties();
    simple_logger::init_with_level(get_log_level_from_env()).unwrap();

    let rabbit_sleep_time = env::var("RABBIT_SLEEP_TIME").unwrap().parse::<u64>().unwrap();
    thread::sleep(time::Duration::from_millis(rabbit_sleep_time*1000));

    let case_counter_quantity = env::var("CASE_COUNTER_QUANTITY").unwrap().parse::<u32>().unwrap();
    let date_counter_quantity = env::var("DATE_COUNTER_QUANTITY").unwrap().parse::<u32>().unwrap();
    let region_counter_quantity = env::var("REGION_COUNTER_QUANTITY").unwrap().parse::<u32>().unwrap();
    let mut connection = Connection::insecure_open(&env::var("RABBITMQ_ADDR").unwrap()).unwrap();
    info!("Connected to RabbitMQ!");
    let channel = connection.open_channel(None).unwrap();
    info!("going to send a message to Counters!");


    let region_exchange = channel.exchange_declare(ExchangeType::Fanout, "region_exchange", ExchangeDeclareOptions::default()).unwrap();
    let region_queue = channel.queue_declare("region-reader-q", QueueDeclareOptions::default()).unwrap();
    let region_consumer = region_queue.consume(ConsumerOptions::default()).unwrap();
    for (_, message) in region_consumer.receiver().iter().enumerate() {
        match message {
            ConsumerMessage::Delivery(delivery) => {
                let body = String::from_utf8_lossy(&delivery.body);
                info!("Got region: {}", body);
                region_exchange.publish(Publish::new(body.as_bytes(), "")).unwrap();
                if body == "EOF" {
                    info!("Finshed processing regions");
                    region_consumer.ack(delivery).unwrap();
                    break;
                }
                region_consumer.ack(delivery).unwrap();
            }
            other => {
                info!("Consumer ended: {:?}", other);
                break;
            }
        }
    }


    let mut total_records = 0;
    let mut total_deaths = 0;
    let mut total_positives = 0;
    let exchange = Exchange::direct(&channel);
    let cases_queue = channel.queue_declare("reader-q", QueueDeclareOptions::default()).unwrap();
    let cases_consumer = cases_queue.consume(ConsumerOptions::default()).unwrap();
    for (_, message) in cases_consumer.receiver().iter().enumerate() {
        match message {
            ConsumerMessage::Delivery(delivery) => {
                let body = String::from_utf8_lossy(&delivery.body);
                if body == "EOF" {
                    info!("Got EOF from reader");
                    cases_consumer.ack(delivery).unwrap();
                    break;
                }
                let message: Vec<&str> = body.split("//").collect();
                total_records = total_records + 1;
                if message[0] == "positivi" {
                    total_positives = total_positives + 1;
                } else if message[0] == "deceduti" {
                    total_deaths = total_deaths + 1;
                } else {
                    info!("Got an unknown type: {}", message[0]);
                }
                exchange.publish(Publish::new(message[0].as_bytes(), "case-counter-q")).unwrap();
                let date_counter_message = format!("{}{}", if message[0] == "positivi" {"P"} else {"D"}, message[3]);
                exchange.publish(Publish::new(date_counter_message.as_bytes(), "date-counter-q")).unwrap();
                if message[0] == "positivi" {
                    exchange.publish(Publish::new(format!("{}//{}", message[1], message[2]).as_bytes(), "region-counter-q")).unwrap();
                }
                cases_consumer.ack(delivery).unwrap();
            }
            other => {
                info!("Consumer ended: {:?}", other);
                break;
            }
        }
    }
    for _ in 0..case_counter_quantity {
        exchange.publish(Publish::new("EOF".as_bytes(), "case-counter-q")).unwrap();
    }
    for _ in 0..date_counter_quantity {
        exchange.publish(Publish::new("EOF".as_bytes(), "date-counter-q")).unwrap();
    }
    for _ in 0..region_counter_quantity {
        exchange.publish(Publish::new("EOF".as_bytes(), "region-counter-q")).unwrap();
    }

    info!("********** total records: {}", total_records);
    info!("********** total positives: {}", total_positives);
    info!("********** total deaths: {}", total_deaths);
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