from config_reader.config_reader import ConfigReader
from multiprocessing import Process, Queue
from watcher.watcher import Watcher
from node_raiser.node_raiser import NodeRaiser
from node_checker.node_checker import NodeChecker
import time

CONFIG_FILE = "config/start_config.json"

class ProcessManager:
    def __init__(self, leader_manager):
        self.leader_manager = leader_manager
        self.processes = []

    def start(self):
        self.leader_manager.start(
            self.new_leader,
            self.disposed_leader
        )
    
        for p in self.processes:
            p.join()
    
    def new_leader(self):
        #Im the new leader
        print("Im the new leader")

        update_queue = Queue()
        dead_queue = Queue()

        health_p = Process(
            target=self.health_process,
            args=(update_queue, )
        )

        checker_p = Process(
            target=self.system_checker_process,
            args=(update_queue, dead_queue)
        )

        raiser_p = Process(
            target=self.raiser_process,
            args=(dead_queue, )
        )
      
        self.processes.append(health_p)
        self.processes.append(checker_p)
        self.processes.append(raiser_p)

        for p in self.processes:
            p.start()

    def disposed_leader(self):
        print("Someone stole my leadership")
        for p in self.processes:
            if p.is_alive():
                p.terminate()
            
        self.processes = []

    def system_checker_process(self, update_queue, dead_queue):
        '''checker = NodeChecker(
            update_queue,
            dead_queue,
            CONFIG_FILE
        )

        checker.start() '''  
        while True:
            print("System checker working")
            time.sleep(3)

    def raiser_process(self, dead_queue):
        '''raiser = NodeRaiser(
            dead_queue
        )

        raiser.start()'''
        while True:  
            print("System raiser working")
            time.sleep(3)        

    def health_process(self, update_queue):
        '''config_params = ConfigReader().parse_vars(
            ["INIT_QUEUE"]
        )
        
        watcher = Watcher(
            config_params["INIT_QUEUE"],
            update_queue
        )

        watcher.start()'''
        while True:  
            print("Health working")
            time.sleep(3)            
