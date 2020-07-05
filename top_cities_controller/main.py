#!/usr/bin/env python3
from top_cities_controller.top_cities_controller import TopCitiesController

from config_reader.config_reader import ConfigReader

def main():
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE",
        "SEND_QUEUE",
        "TOTAL_WORKERS"]
    )

    worker = TopCitiesController(
        config_params["RECV_QUEUE"],
        config_params["SEND_QUEUE"],
        int(config_params["TOTAL_WORKERS"])
    )

    worker.start()

if __name__== "__main__":
    main()
