# Initial list of project tasks
tasks = [
    "Design the UI",
    "Develop the backend",
    "Write documentation",
    "Test the application",
    "Deploy to production"
]

print("Initial list of tasks:")
for i, task in enumerate(tasks, 1):
    print(f"  {i}. {task}")

# Prompt the user to input the number of the task to remove
task_number = int(input("Enter the number of the task to remove: "))

# Validate the task number
if 1 <= task_number <= len(tasks):
    task_to_remove = tasks[task_number - 1]
    tasks.remove(task_to_remove)
    print(f"\nTask '{task_to_remove}' has been removed.")
else:
    print(f"\nInvalid task number: {task_number}")

print("\nList of tasks after removal:")
for i, task in enumerate(tasks, 1):
    print(f"  {i}. {task}")

# Reverse the order of tasks
tasks.reverse()

print("\nList of tasks after reversing:")
for i, task in enumerate(tasks, 1):
    print(f"  {i}. {task}")
