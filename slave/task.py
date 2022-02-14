

class Task:

    def __init__(self, task_id: str, tasker: str, query: str, execution_time: float):
        self.id = task_id
        self.tasker = tasker  # IP address of master-node
        self.query = query  # execution sequence of task
        self.execution_time = execution_time
        self.status = 'DORMANT'
        self.logs = []

    def run_task(self):
        self.status = 'RUNNING'
        self.data = self.query
        self.status = 'COMPLETE'
        return self.data
