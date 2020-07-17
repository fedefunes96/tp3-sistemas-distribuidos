import subprocess
import os
import sys

class NodeRaiser:
    def __init__(self, dead_queue):
        self.dead_queue = dead_queue

    def start(self):
        while True:
            [worker_id, worker_type] = self.dead_queue.get()

            print("Dead node received: {} {}".format(worker_id, worker_type))

            self.raise_node(worker_id, worker_type)

    def raise_node(self, worker_id, worker_type):
        #process = "dockerfromdocker_" + worker_id
        '''result = subprocess.run(
            ['docker', 'stop', process],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )'''

        result = subprocess.run(['echo', 'world'], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('Command executed. Result={}. Output={}. Error={}'.format(result.returncode, result.stdout, result.stderr))
