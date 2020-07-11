#!/usr/bin/env python3
from master_controller.master_controller import MasterController

from config_reader.config_reader import ConfigReader
from status_checker.status_checker import StatusChecker
from multiprocessing import Process

def main_process():
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE",
        "SEND_QUEUE",
        "TOTAL_WORKERS"]
    )

    master_controller = MasterController(
        config_params["RECV_QUEUE"],
        config_params["SEND_QUEUE"],
        int(config_params["TOTAL_WORKERS"])
    )

    master_controller.start()

def main():
    p = Process(target=main_process)
    p.start()

    checker = StatusChecker(p)

    checker.start()

    p.join()

if __name__== "__main__":
    main()
