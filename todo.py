import uuid
from datetime import datetime

class Task:
    def __init__(self, description, deadline=None, priority="Medium", completed=False):
        self.id = str(uuid.uuid4())
        self.description = description
        self.deadline = deadline  # Format: YYYY-MM-DD
        self.priority = priority  # High, Medium, Low
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "deadline": self.deadline,
            "priority": self.priority,
            "completed": self.completed,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["description"],
            deadline=data.get("deadline"),
            priority=data.get("priority", "Medium"),
            completed=data["completed"]
        )


class ToDoManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, deadline=None, priority="Medium"):
        task = Task(description, deadline=deadline, priority=priority)
        self.tasks.append(task)
        return task

    def list_tasks(self):
        return self.tasks

    def update_task(self, task_id, description=None, deadline=None, priority=None, completed=None):
        for task in self.tasks:
            if task.id == task_id:
                if description is not None:
                    task.description = description
                if deadline is not None:
                    task.deadline = deadline
                if priority is not None:
                    task.priority = priority
                if completed is not None:
                    task.completed = completed
                return task
        raise ValueError("Task not found")

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
