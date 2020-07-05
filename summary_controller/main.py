#!/usr/bin/env python3
from summary_controller.summary_controller import SummaryController

from config_reader.config_reader import ConfigReader

def main():
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE"]
    )

    master_controller = SummaryController(
        config_params["RECV_QUEUE"],
    )

    master_controller.start()

if __name__== "__main__":
    main()
