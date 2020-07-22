#!/usr/bin/env python3
from worker.worker import Worker

from config_reader.config_reader import ConfigReader
from status_checker.status_checker import StatusChecker
from multiprocessing import Process


def main_process():
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE",
         "SEND_QUEUE",
         "STATUS_QUEUE"]
    )

    worker = Worker(
        config_params["RECV_QUEUE"],
        config_params["SEND_QUEUE"],
        config_params["STATUS_QUEUE"]
    )

    worker.start()


def main():
    p = Process(target=main_process)
    p.start()

    params = ConfigReader().parse_vars(["STATUS_QUEUE"])

    checker = StatusChecker([p], params["STATUS_QUEUE"])

    checker.start()

    p.join()


if __name__ == "__main__":
    main()
