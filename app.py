from todo import ToDoManager
from storage import StorageManager

def print_menu():
    print("\n--- To-Do List Menu ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")

def main():
    manager = ToDoManager()
    manager.tasks = StorageManager.load_from_file()

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            task = manager.add_task(description)
            print(f"Task added with ID: {task.id}")
        elif choice == "2":
            tasks = manager.list_tasks()
            if not tasks:
                print("No tasks found.")
            for task in tasks:
                status = "Done" if task.completed else "Pending"
                print(f"{task.id}: {task.description} [{status}]")
        elif choice == "3":
            task_id = input("Enter task ID to update: ")
            description = input("New description (leave blank to skip): ")
            completed = input("Mark as completed? (yes/no/leave blank): ").lower()
            try:
                manager.update_task(
                    task_id,
                    description=description if description else None,
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
            print("Tasks saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
