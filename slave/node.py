from .task_executor import TaskManager
from .storage import Storage
from .config import port, protocol
from requests import post


class Node:
    def __init__(self, master: str):
        self.master_node = master
        self.info = self.connect(master)
        self.storage = Storage(self.info['id'])
        self.task_manager = TaskManager(self)

    @staticmethod
    def connect(master: str):
        print(master)
        response = post(f"{master}/nodes", data={'protocol': protocol, 'port': port})
        response.raise_for_status()

        return response.json()
