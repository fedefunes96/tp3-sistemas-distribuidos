from config_reader.config_reader import ConfigReader
from multiprocessing import Process
from cluster_manager.replica_manager import ReplicaManager
from cluster_manager.read_manager import ReadManager
from cluster_manager.write_manager import WriteManager
import time

ROUTE = "data/"

class ProcessManager:
    def __init__(self, leader_manager):
        self.leader_manager = leader_manager
        self.processes = []

    def start(self):
        self.start_as_replica()

        self.leader_manager.start(
            self.new_leader,
            self.disposed_leader
        )

    def start_as_replica(self):
        self.reader_p = Process(
            target=self.read_manager_process
        )

        self.replica_p = Process(
            target=self.replica_manager_process
        )

        self.reader_p.start()
        self.replica_p.start()
    
    def new_leader(self):
        #Im the new leader
        print("Im the new leader")

        #Finish replica process and delete its queue content
        if self.replica_p.is_alive():
            self.replica_p.terminate()
        
        self.writer_p = Process(
            target=self.write_manager_process
        )

        self.writer_p.start()

    def disposed_leader(self):
        print("Someone stole my leadership")

        #Stop working as a leader who receives writes
        if self.writer_p.is_alive():
            self.writer_p.terminate()

        self.replica_p = Process(
            target=self.replica_manager_process
        )

        self.replica_p.start()

    def write_manager_process(self):
        print("Starting write manager")

        config_params = ConfigReader().parse_vars(
            ["RECV_WRITE_QUEUE", "RECV_REPLICA_A", "RECV_REPLICA_B"]
        )

        write_manager = WriteManager(
            ROUTE, 
            config_params["RECV_WRITE_QUEUE"],
            [config_params["RECV_REPLICA_A"], config_params["RECV_REPLICA_B"]]
        )

        write_manager.start()

    def read_manager_process(self):
        print("Starting read manager")

        config_params = ConfigReader().parse_vars(
            ["RECV_READ_QUEUE"]
        )

        read_manager = ReadManager(
            ROUTE,
            config_params["RECV_READ_QUEUE"]
        )

        read_manager.start()       

    def replica_manager_process(self):
        print("Starting replica manager")

        config_params = ConfigReader().parse_vars(
            ["RECV_REPLICA"]
        )

        replica_manager = ReplicaManager(
            ROUTE,
            config_params["RECV_REPLICA"]
        )

        replica_manager.start()
