#!/usr/bin/env python3

from config_reader.config_reader import ConfigReader
from multiprocessing import Process, Queue
from watcher.watcher import Watcher

CONFIG_FILE = "config/start_config.txt"

    def initialize_workers(config_file):
        initial_workers = ConfigReader().parse_from_file(config_file)

        for worker_type in initial_workers:
            for number_workers in range(0, initial_workers[worker_type]):
                self.raise_up_worker(worker_type)


def health_process(queue):
    

def main():
    config_params = ConfigReader().parse_vars(
        ["INIT_QUEUE"]
    )
    
    watcher = Watcher(
        config_params["INIT_QUEUE"]
    )

    watcher.start(CONFIG_FILE)

if __name__== "__main__":
    main()
