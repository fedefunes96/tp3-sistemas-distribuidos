#!/usr/bin/env python3
from places_manager.place_receiver import PlaceReceiver
from places_manager.place_requester import PlaceRequester

from config_reader.config_reader import ConfigReader
from status_checker.status_checker import StatusChecker
from multiprocessing import Process, Queue

def receiver_process():
    config_params = ConfigReader().parse_vars(
        [
            "RECV_QUEUE", 
            "DATA_CLUSTER_WRITE",
            "DATA_CLUSTER_READ",
            "RECV_REQUEST_QUEUE"
        ]
    )

    worker = PlaceReceiver(
        config_params["RECV_QUEUE"],
        config_params["RECV_REQUEST_QUEUE"],
        config_params["DATA_CLUSTER_WRITE"],
        config_params["DATA_CLUSTER_READ"]        
    )

    while True:
        worker.start()

def main():
    receiver_p = Process(target=receiver_process)
    receiver_p.start()

    params = ConfigReader().parse_vars(["STATUS_QUEUE", "WORKER_ID", "WORKER_TYPE"])

    checker = StatusChecker(
        params["WORKER_ID"],
        params["WORKER_TYPE"],
        [receiver_p],
        params["STATUS_QUEUE"]
    )

    checker.start()

    receiver_p.join()

if __name__== "__main__":
    main()
