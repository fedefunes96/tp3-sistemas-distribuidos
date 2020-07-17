#!/usr/bin/env python3

from date_sorter.date_sorter import DateSorter

from config_reader.config_reader import ConfigReader
from status_checker.status_checker import StatusChecker
from multiprocessing import Process

def main_process():
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE",
        "SEND_QUEUE",
        "TOTAL_WORKERS"]
    )

    worker = DateSorter(
        config_params["RECV_QUEUE"],
        config_params["SEND_QUEUE"],
        int(config_params["TOTAL_WORKERS"])
    )

    worker.start()

def main():
    p = Process(target=main_process)
    p.start()

    params = ConfigReader().parse_vars(["STATUS_QUEUE"])

    checker = StatusChecker([p], params["STATUS_QUEUE"])

    checker.start()

    p.join()

if __name__== "__main__":
    main()
