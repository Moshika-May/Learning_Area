# Initial to-do list
todo_list = {
    'task1': {'priority': 'high', 'description': 'Finish the report'},
    'task2': {'priority': 'medium', 'description': 'Email the client'},
    'task3': {'priority': 'low', 'description': 'Update the project plan'},
    'task4': {'priority': 'high', 'description': 'Prepare for the meeting'}
}

def print_todo_list(todo_list):
    """Prints the to-do list."""
    print("\nCurrent To-Do List:")
    for task, details in todo_list.items():
        print(f"Task: {task}, Priority: {details['priority']}, Description: {details['description']}")

def complete_task(todo_list):
    """Allows user to mark a task as completed and remove it from the to-do list."""
    task = input("Enter the name of the task you have completed: ")
    details = todo_list.pop(task, None)
    if details:
        print(f"Completed and removed task: {task}, Details: {details}")
    else:
        print(f"Task {task} not found in the to-do list.")

def main():
    while True:
        print("\nTo-Do List Management Menu")
        print("1. Display to-do list")
        print("2. Mark task as completed")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            print_todo_list(todo_list)
        elif choice == '2':
            complete_task(todo_list)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

main()
