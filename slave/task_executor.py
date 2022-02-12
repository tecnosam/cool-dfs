import concurrent.futures
from typing import Dict
from .task import Task
import time


class TaskManager:
    def __init__(self, node):
        self.tasks: Dict[str, Task] = dict()
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.schedule = []
        self.node = node

    def add_task(self, task: Task):
        self.tasks[task.id] = task

        if not task.execution_time:
            self.process_task(task)
        else:
            self.schedule.append(task.id)

    def process_task(self, task: Task):

        if task.execution_time <= time.time():
            p = self.executor.submit(task.run_task)
            p.add_done_callback(lambda x: x)
            return p

        return None

    def task_callback(self, result):
        # todo: ideally, should communicate desired output to master node
        # will need to communicate with node.net_interface
        pass
