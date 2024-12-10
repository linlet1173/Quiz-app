import json
from todo import Task

class StorageManager:
    @staticmethod
    def save_to_file(tasks, filename="tasks.json"):
        with open(filename, "w") as f:
            json.dump([task.to_dict() for task in tasks], f)

    @staticmethod
    def load_from_file(filename="tasks.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except FileNotFoundError:
            return []
