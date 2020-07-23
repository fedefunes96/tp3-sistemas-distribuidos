#!/usr/bin/env python3
from summary_controller.summary_controller import SummaryController

from config_reader.config_reader import ConfigReader
from status_checker.status_checker import StatusChecker
from multiprocessing import Process

def main_process():
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE", "STATUS_QUEUE"]
    )

    master_controller = SummaryController(
        config_params["RECV_QUEUE"],
        config_params["STATUS_QUEUE"],
    )

    master_controller.start()

def main():
    p = Process(target=main_process)
    p.start()

    params = ConfigReader().parse_vars(["STATUS_QUEUE", "WORKER_ID", "WORKER_TYPE"])

    checker = StatusChecker(
        params["WORKER_ID"],
        params["WORKER_TYPE"],
        [p], 
        params["STATUS_QUEUE"]
    )

    checker.start()

    p.join()

if __name__== "__main__":
    main()
