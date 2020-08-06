#!/usr/bin/env python3

from config_reader.config_reader import ConfigReader
from synchronization.bully_leader import BullyLeader
from synchronization.node.node import Node
from process_manager.process_manager import ProcessManager

def main():
    print("Starting Cluster Node")

    config_params = ConfigReader().parse_vars(
        ["MY_ID", "MY_DIR", "PORT"]
    )

    nodes_ids = [
    ]

    my_node = Node(config_params["MY_ID"], config_params["MY_DIR"])

    bully_leader = BullyLeader(
        my_node,
        int(config_params["PORT"]),
        nodes_ids
    )

    process_manager = ProcessManager(bully_leader)

    process_manager.start()

if __name__== "__main__":
    main()
