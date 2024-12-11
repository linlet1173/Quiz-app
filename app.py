from flask import Flask, render_template, request, redirect, url_for
from todo import ToDoManager
from storage import StorageManager
from datetime import datetime

app = Flask(__name__)

# Initialize ToDoManager and load tasks from storage
manager = ToDoManager()
manager.tasks = StorageManager.load_from_file()

def check_overdue_tasks(tasks):
    today = datetime.today().date()
    overdue = []
    for task in tasks:
        if task.deadline:
            try:
                deadline_str = task.deadline.split(",")[0]
                deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                if deadline_date < today and not task.completed:
                    overdue.append(task)
            except ValueError:
                pass
    return overdue

@app.route('/')
def index():
    overdue_tasks = check_overdue_tasks(manager.tasks)
    tasks = manager.list_tasks()
    return render_template('index.html', tasks=tasks, overdue_tasks=overdue_tasks)

@app.route('/add', methods=['POST'])
def add_task():
    description = request.form.get('description')
    deadline = request.form.get('deadline') or None
    priority = request.form.get('priority') or "Medium"
    if description:
        manager.add_task(description, deadline=deadline, priority=priority)
        StorageManager.save_to_file(manager.list_tasks())
    return redirect(url_for('index'))

@app.route('/delete/<task_id>')
def delete_task(task_id):
    manager.delete_task(task_id)
    StorageManager.save_to_file(manager.list_tasks())
    return redirect(url_for('index'))

@app.route('/update/<task_id>', methods=['POST'])
def update_task(task_id):
    description = request.form.get('description') or None
    deadline = request.form.get('deadline') or None
    priority = request.form.get('priority') or None
    completed = request.form.get('completed') == "on"
    try:
        manager.update_task(task_id, description=description, deadline=deadline, priority=priority, completed=completed)
        StorageManager.save_to_file(manager.list_tasks())
    except ValueError as e:
        print(str(e))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
