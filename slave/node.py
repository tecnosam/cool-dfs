from .task_executor import TaskManager
from .storage import Storage


class Node:
    def __init__(self, master: tuple):
        self.master_node = master
        self.node_id = self.connect(master)
        self.storage = Storage(self.node_id, 1024)
        self.task_manager = TaskManager(self)

    @staticmethod
    def connect(master: tuple):
        # todo connect to master and get ID
        print(master)
        return "1"
