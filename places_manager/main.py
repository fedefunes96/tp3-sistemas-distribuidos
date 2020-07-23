#!/usr/bin/env python3
from places_manager.place_receiver import PlaceReceiver
from places_manager.place_requester import PlaceRequester

from config_reader.config_reader import ConfigReader
from status_checker.status_checker import StatusChecker
from multiprocessing import Process, Queue

def receiver_process(queue):
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE"]
    )

    worker = PlaceReceiver(
        config_params["RECV_QUEUE"],
        queue
    )

    worker.start()

def requester_process(queue):
    config_params = ConfigReader().parse_vars(
        ["RECV_REQUEST_QUEUE"]
    )

    working = True
    
    while working:
        worker = PlaceRequester(
            config_params["RECV_REQUEST_QUEUE"],
            queue
        )

        working = worker.start()

def main():
    queue = Queue()

    receiver_p = Process(target=main_process, args=(queue, ))
    receiver_p.start()

    requester_p = Process(target=requester_process, args=(queue, ))
    requester_p.start()    

    params = ConfigReader().parse_vars(["STATUS_QUEUE", "WORKER_ID", "WORKER_TYPE"])

    checker = StatusChecker(
        params["WORKER_ID"],
        params["WORKER_TYPE"],
        [receiver_p, requester_p], 
        params["STATUS_QUEUE"]
    )

    checker.start()

    receiver_p.join()
    requester_p.join()

if __name__== "__main__":
    main()
