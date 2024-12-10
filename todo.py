import uuid

class Task:
    def __init__(self, description, completed=False):
        self.id = str(uuid.uuid4())
        self.description = description
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(data["description"], data["completed"])


class ToDoManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        task = Task(description)
        self.tasks.append(task)
        return task

    def list_tasks(self):
        return self.tasks

    def update_task(self, task_id, description=None, completed=None):
        for task in self.tasks:
            if task.id == task_id:
                if description is not None:
                    task.description = description
                if completed is not None:
                    task.completed = completed
                return task
        raise ValueError("Task not found")

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
