#!/usr/bin/env python3
from coordinator_manager.coordinator_manager import CoordinatorManager

from config_reader.config_reader import ConfigReader
from status_checker.status_checker import StatusChecker
from multiprocessing import Process

def main_process():
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE", "TOTAL_DATE_WORKERS", "TOTAL_MAP_WORKERS",
        "TOTAL_SINGLE_MAP_WORKERS", "TOTAL_COUNT_WORKERS",
        "DATA_CLUSTER_WRITE", "DATA_CLUSTER_READ"]
    )

    senders = []

    for i in range(0, int(config_params["TOTAL_DATE_WORKERS"])):
        senders.append("date_worker_" + str(i + 1))

    for i in range(0, int(config_params["TOTAL_COUNT_WORKERS"])):
        senders.append("count_worker_" + str(i + 1))

    for i in range(0, int(config_params["TOTAL_MAP_WORKERS"])):
        for j in range(0, int(config_params["TOTAL_SINGLE_MAP_WORKERS"])):
            senders.append("map_worker_" + str(i + 1) + "__" + str(j))   

    senders.append("place_manager_request")

    worker = CoordinatorManager(
        config_params["RECV_QUEUE"],
        senders,
        config_params["DATA_CLUSTER_WRITE"],
        config_params["DATA_CLUSTER_READ"]
    )

    worker.start()


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


if __name__ == "__main__":
    main()
