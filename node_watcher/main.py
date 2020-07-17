#!/usr/bin/env python3

from config_reader.config_reader import ConfigReader
from multiprocessing import Process, Queue
from watcher.watcher import Watcher
from node_raiser.node_raiser import NodeRaiser
from node_checker.node_checker import NodeChecker

CONFIG_FILE = "config/start_config.txt"

    def initialize_workers(config_file):
        initial_workers = ConfigReader().parse_from_file(config_file)

        for worker_type in initial_workers:
            for number_workers in range(0, initial_workers[worker_type]):
                self.raise_up_worker(worker_type)

def system_checker_process(update_queue, dead_queue):
    checker = NodeChecker(
        update_queue,
        dead_queue
    )

    checker.start()   

def raiser_process(dead_queue):
    raiser = NodeRaiser(
        dead_queue
    )

    raiser.start()  

def health_process(update_queue):
    config_params = ConfigReader().parse_vars(
        ["INIT_QUEUE"]
    )
    
    watcher = Watcher(
        config_params["INIT_QUEUE"],
        update_queue
    )

    watcher.start()    

def main():
    update_queue = Queue()
    dead_queue = Queue()

    health_p = Process(target=health_process, args=(update_queue, ))
    health_p.start()

    checker_p = Process(target=system_checker_process, args=(update_queue, dead_queue))
    checker_p.start()

    raiser_p = Process(target=raiser_process, args=(dead_queue, ))
    raiser_p.start()

    health_p.join()
    checker_p.join()
    raiser_p.join()

if __name__== "__main__":
    main()
