#!/usr/bin/env python3
from summary_controller.summary_controller import SummaryController

from config_reader.config_reader import ConfigReader
from status_checker.status_checker import StatusChecker
from multiprocessing import Process

def main_process():
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE"]
    )

    master_controller = SummaryController(
        config_params["RECV_QUEUE"],
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
