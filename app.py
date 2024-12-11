from flask import Flask, render_template, request, redirect, url_for
from todo import ToDoManager
from storage import StorageManager
from datetime import datetime

app = Flask(__name__)

# Initialize the ToDoManager and load tasks from storage
manager = ToDoManager()
manager.tasks = StorageManager.load_from_file()

@app.route("/")
def index():
    # Show all tasks by default
    tasks = manager.list_tasks()
    overdue_tasks = [
        task for task in tasks if task.deadline and datetime.strptime(task.deadline, "%Y-%m-%d").date() < datetime.today().date() and not task.completed
    ]
    task_count = len(tasks)
    return render_template("index.html", tasks=tasks, overdue_tasks=overdue_tasks, task_count=task_count)


@app.route("/filter", methods=["GET"])
def filter_tasks():
    tasks = manager.list_tasks()
    filter_by = request.args.get("filter_by")

    if filter_by == "priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        tasks.sort(key=lambda t: priority_order.get(t.priority, 3))
    elif filter_by == "deadline":
        tasks.sort(key=lambda t: datetime.strptime(t.deadline, "%Y-%m-%d").date() if t.deadline else datetime.max.date())
    elif filter_by == "status":
        tasks.sort(key=lambda t: t.completed)

    return render_template("index.html", tasks=tasks, overdue_tasks=[])


@app.route("/add", methods=["POST"])
def add_task():
    description = request.form["description"]
    deadline = request.form.get("deadline")
    priority = request.form.get("priority", "Medium")
    manager.add_task(description, deadline=deadline or None, priority=priority)
    return redirect(url_for("index"))


@app.route("/update/<task_id>", methods=["POST"])
def update_task(task_id):
    manager.update_task(task_id, completed=True)
    return redirect(url_for("index"))


@app.route("/delete/<task_id>", methods=["GET"])
def delete_task(task_id):
    manager.delete_task(task_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Save tasks when the app is shut down
    try:
        app.run(debug=True)
    finally:
        StorageManager.save_to_file(manager.list_tasks())
