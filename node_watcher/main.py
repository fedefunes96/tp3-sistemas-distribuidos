#!/usr/bin/env python3

from config_reader.config_reader import ConfigReader
from watcher.watcher import Watcher

CONFIG_FILE = "config/start_config.txt"

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
