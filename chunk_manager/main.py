#!/usr/bin/env python3

from config_reader.config_reader import ConfigReader
from chunk_manager.chunk_manager import ChunkManager

DATA_FILE = 'data/data.csv'
PLACE_FILE = 'data/places.csv'

def main():
    config_params = ConfigReader().parse_vars(
        ["QUEUE_MAP",
        "QUEUE_DATE",
        "QUEUE_COUNT",
        "EOF_MAP",
        "EOF_DATE",
        "EOF_COUNT",
        "TOPIC_PLACES"]
    )
    
    chunk_manager = ChunkManager(
        config_params["QUEUE_MAP"],
        config_params["QUEUE_DATE"],
        config_params["QUEUE_COUNT"],
        config_params["EOF_MAP"],
        config_params["EOF_DATE"],
        config_params["EOF_COUNT"],
        config_params["TOPIC_PLACES"]    
    )

    chunk_manager.process_places(PLACE_FILE)
    chunk_manager.process_data(DATA_FILE)

if __name__== "__main__":
    main()
