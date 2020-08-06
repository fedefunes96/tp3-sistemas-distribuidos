#!/usr/bin/env python3
from worker.worker import Worker

from config_reader.config_reader import ConfigReader
from status_checker.status_checker import StatusChecker
from multiprocessing import Process

def main_process(my_id):
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE",
        "SEND_QUEUE",
        "MASTER_SEND_QUEUE",
        "SEND_REQUEST_QUEUE",
        "STATUS_QUEUE",
        "DATA_CLUSTER_WRITE",
        "DATA_CLUSTER_READ"
        ]
    )

    worker = Worker(
        config_params["RECV_QUEUE"],
        [config_params["SEND_QUEUE"]],
        config_params["MASTER_SEND_QUEUE"],
        config_params["SEND_REQUEST_QUEUE"],
        config_params["STATUS_QUEUE"],
        config_params["DATA_CLUSTER_WRITE"],
        config_params["DATA_CLUSTER_READ"],
        my_id
    )
    
    while True:
        worker.start()

def generate_worker_id(sub_id, main_id):
    return main_id + "__" + sub_id

def main():
    params = ConfigReader().parse_vars(["STATUS_QUEUE", "WORKERS", "WORKER_ID", "WORKER_TYPE"])

    processes = []

    worker_id = 0

    for worker in range(0, int(params["WORKERS"])):
        my_id = generate_worker_id(str(worker_id), params["WORKER_ID"])
        p = Process(target=main_process, args=(my_id, ))
        p.start()
        processes.append(p)
        worker_id += 1

    checker = StatusChecker(
        params["WORKER_ID"],
        params["WORKER_TYPE"],
        processes, 
        params["STATUS_QUEUE"]
    )
    checker.start()
    print("Joining processes")
    for p in processes:
        print("joining one process")
        p.join()
        print("Process joined")

if __name__== "__main__":
    main()
