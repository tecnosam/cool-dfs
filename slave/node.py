from .task_executor import TaskManager
from .storage import Storage


class Node:
    def __init__(self, master: tuple, storage_size=1024):
        self.master_node = master
        self.node_id = self.connect(master)
        self.storage = Storage(self.node_id, storage_size)
        self.task_manager = TaskManager(self)

    @staticmethod
    def connect(master: tuple):
        # todo connect to master and get ID
        print(master)
        return "1"
