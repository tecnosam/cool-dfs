from task_executor import TaskManager
from storage import Storage


class Node:
    def __init__(self, node_id: str, master: tuple, port: int):
        self.master_node = master
        self.storage = Storage(node_id, 1024)
        self.task_manager = TaskManager(self)
