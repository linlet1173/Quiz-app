from todo import ToDoManager
from storage import StorageManager
from datetime import datetime

def print_menu():
    print("\n--- To-Do List Menu ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")

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
            except ValueError as e:
                print(f"Error parsing deadline '{task.deadline}': {e}")
    if overdue:
        print("\n** Overdue Tasks **")
        for task in overdue:
            print(f"{task.id}: {task.description} (Deadline: {task.deadline})")

def display_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return

    print("\n--- Task List ---")
    for i, task in enumerate(tasks, start=1):
        status = "Done" if task.completed else "Pending"
        print(f"{i}. {task.id}: {task.description}")
        print(f"   - Deadline: {task.deadline or 'None'}")
        print(f"   - Priority: {task.priority}")
        print(f"   - Status: {status}\n")

def main():
    manager = ToDoManager()
    manager.tasks = StorageManager.load_from_file()

    # Notify user about overdue tasks
    check_overdue_tasks(manager.tasks)

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            deadline = input("Enter deadline (YYYY-MM-DD, leave blank if none): ")
            priority = input("Enter priority (High/Medium/Low, default is Medium): ") or "Medium"
            task = manager.add_task(description, deadline=deadline or None, priority=priority)
            print(f"Task added with ID: {task.id}")

        elif choice == "2":
            tasks = manager.list_tasks()

            print("\n--- View Tasks ---")
            print("1. Sort by Deadline")
            print("2. Sort by Priority")
            print("3. Sort by Status (Pending/Completed)")
            print("4. View All Tasks (Unsorted)")
            view_choice = input("Enter your choice: ")

            if view_choice == "1":
                tasks.sort(key=lambda t: datetime.strptime(t.deadline, "%Y-%m-%d").date() if t.deadline else datetime.max.date())
            elif view_choice == "2":
                priority_order = {"High": 1, "Medium": 2, "Low": 3}
                tasks.sort(key=lambda t: priority_order.get(t.priority, 3))
            elif view_choice == "3":
                tasks.sort(key=lambda t: t.completed)
            elif view_choice != "4":
                print("Invalid choice. Showing all tasks unsorted.")

            display_tasks(tasks)

        elif choice == "3":
            task_id = input("Enter task ID to update: ")
            description = input("New description (leave blank to skip): ")
            deadline = input("New deadline (YYYY-MM-DD, leave blank to skip): ")
            priority = input("New priority (High/Medium/Low, leave blank to skip): ")
            completed = input("Mark as completed? (yes/no/leave blank): ").lower()
            try:
                manager.update_task(
                    task_id,
                    description=description if description else None,
                    deadline=deadline if deadline else None,
                    priority=priority if priority else None,
                    completed=(completed == "yes") if completed else None,
                )
                print("Task updated successfully.")
            except ValueError as e:
                print(str(e))

        elif choice == "4":
            task_id = input("Enter task ID to delete: ")
            manager.delete_task(task_id)
            print("Task deleted successfully.")

        elif choice == "5":
            tasks_to_save = manager.list_tasks()
            if isinstance(tasks_to_save, list):
                StorageManager.save_to_file(tasks_to_save)
                print("Tasks saved. Goodbye! Have a lovely day!")
            else:
                print("Error: Failed to retrieve tasks for saving.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
