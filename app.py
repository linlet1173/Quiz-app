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
    overdue = [task for task in tasks if task.deadline and datetime.strptime(task.deadline, "%Y-%m-%d").date() < today and not task.completed]
    if overdue:
        print("\n** Overdue Tasks **")
        for task in overdue:
            print(f"{task.id}: {task.description} (Deadline: {task.deadline})")

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
            if not manager.list_tasks():
                print("No tasks found.")
                continue

            print("\n--- View Tasks ---")
            print("1. Sort by Deadline")
            print("2. Sort by Priority")
            print("3. Sort by Status (Pending/Completed)")
            print("4. View All Tasks (Unsorted)")
            view_choice = input("Enter your choice: ")

            tasks = manager.list_tasks()

            if view_choice == "1":
                # Sort by deadline (None values at the end)
                tasks.sort(key=lambda t: t.deadline or "9999-12-31")
            elif view_choice == "2":
                # Sort by priority (High -> Medium -> Low)
                priority_order = {"High": 1, "Medium": 2, "Low": 3}
                tasks.sort(key=lambda t: priority_order.get(t.priority, 3))
            elif view_choice == "3":
                # Sort by completion status (Pending first, Completed last)
                tasks.sort(key=lambda t: t.completed)
            elif view_choice == "4":
                # Unsorted view
                pass
            else:
                print("Invalid choice. Showing all tasks unsorted.")

            print("\n--- Task List ---")
            for task in tasks:
                status = "Done" if task.completed else "Pending"
                print(f"{task.id}: {task.description} | Deadline: {task.deadline or 'None'} | Priority: {task.priority} | Status: {status}")

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
            StorageManager.save_to_file(manager.list_tasks())
            print("Tasks saved. Goodbye! Have a lovely day!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
