#!/usr/bin/env python3
from worker.worker import Worker

from config_reader.config_reader import ConfigReader

def main():
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE",
        "SEND_QUEUE",
        "MASTER_SEND_QUEUE",
        "TOPIC_PLACES"]
    )

    worker = Worker(
        config_params["RECV_QUEUE"],
        [config_params["SEND_QUEUE"]],
        config_params["MASTER_SEND_QUEUE"],
        config_params["TOPIC_PLACES"]
    )

    worker.start()

if __name__== "__main__":
    main()
