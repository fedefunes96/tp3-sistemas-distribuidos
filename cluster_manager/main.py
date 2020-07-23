#!/usr/bin/env python3

from config_reader.config_reader import ConfigReader
from synchronization.bully_leader import BullyLeader
from synchronization.node.node import Node
from process_manager.process_manager import ProcessManager

def main():
    print("Starting Cluster Node")

    config_params = ConfigReader().parse_vars(
        #["MY_ID", "MY_DIR", "PORT", "NODE_A", "NODE_B",
        #"ID_A", "ID_B"]
        ["MY_ID", "MY_DIR", "PORT"]
    )

    nodes_ids = [
        #Node(config_params["ID_A"], config_params["NODE_A"]),
        #Node(config_params["ID_B"], config_params["NODE_B"])
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
