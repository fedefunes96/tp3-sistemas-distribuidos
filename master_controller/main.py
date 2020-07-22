#!/usr/bin/env python3
from master_controller.master_controller import MasterController
from resume_master_controller.resume_master_controller import ResumeMasterController

from config_reader.config_reader import ConfigReader
from status_checker.status_checker import StatusChecker
from multiprocessing import Process

def master_process():
    config_params = ConfigReader().parse_vars(
        ["RECV_QUEUE",
        "SEND_QUEUE",
        "TOTAL_WORKERS",
        "STATUS_QUEUE"]
    )

    master_controller = MasterController(
        config_params["RECV_QUEUE"],
        config_params["SEND_QUEUE"],
        int(config_params["TOTAL_WORKERS"]),
        config_params["STATUS_QUEUE"]
    )

    master_controller.start()

def resume_master_process():
    config_params = ConfigReader().parse_vars(
        ["RECV_RESUME_QUEUE",
        "SEND_RESUME_QUEUE",
        "TOTAL_WORKERS"]
    )

    master_controller = ResumeMasterController(
        config_params["RECV_RESUME_QUEUE"],
        config_params["SEND_RESUME_QUEUE"],
        int(config_params["TOTAL_WORKERS"])
    )

    master_controller.start()    

def main():
    master = Process(target=master_process)
    master.start()

    resume_master = Process(target=resume_master_process)
    resume_master.start()

    params = ConfigReader().parse_vars(["STATUS_QUEUE", "WORKER_ID", "WORKER_TYPE"])

    checker = StatusChecker(
        params["WORKER_ID"],
        params["WORKER_TYPE"],
        [master, resume_master], 
        params["STATUS_QUEUE"]
    )

    checker.start()

    master.join()
    resume_master.join()


if __name__== "__main__":
    main()
