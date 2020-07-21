#!/usr/bin/env python3

from config_reader.config_reader import ConfigReader
from multiprocessing import Process, Queue
from watcher.watcher import Watcher
from node_raiser.node_raiser import NodeRaiser
from node_checker.node_checker import NodeChecker
from synchronization.bully_leader import BullyLeader
from synchronization.node.node import Node
from synchronization.leader_manager import LeaderManager

CONFIG_FILE = "config/start_config.json"

def system_checker_process(update_queue, dead_queue):
    checker = NodeChecker(
        update_queue,
        dead_queue,
        CONFIG_FILE
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

def new_leader(node_id):
    print("New leader detected: {}".format(node_id))

def main():
    print("Starting Watcher Node")
    update_queue = Queue()
    dead_queue = Queue()

    #health_p_leader_queue = Queue()
    #checker_p_leader_queue = Queue()
    #raiser_p_leader_queue = Queue()

    #health_p = Process(target=health_process, args=(update_queue, ))
    #health_p.start()

    #checker_p = Process(target=system_checker_process, args=(update_queue, dead_queue))
    #checker_p.start()

    #raiser_p = Process(target=raiser_process, args=(dead_queue, ))
    #raiser_p.start()

    config_params = ConfigReader().parse_vars(
        ["MY_ID", "MY_DIR", "PORT", "NODE_A", "NODE_B", "NODE_C", "NODE_D",
        "ID_A", "ID_B", "ID_C", "ID_D"]
    )

    nodes_ids = [
        Node(config_params["ID_A"], config_params["NODE_A"]),
        Node(config_params["ID_B"], config_params["NODE_B"]),
        Node(config_params["ID_C"], config_params["NODE_C"]),
        Node(config_params["ID_D"], config_params["NODE_D"])
    ]

    bully_leader = BullyLeader(
        Node(config_params["MY_ID"], config_params["MY_DIR"]),
        int(config_params["PORT"]),
        nodes_ids
    )

    processes = [health_p, checker_p, raiser_p]

    leader_manager = LeaderManager(bully_leader, processes)

    leader_manager.start()

    #health_p.join()
    #checker_p.join()
    #raiser_p.join()

if __name__== "__main__":
    main()
