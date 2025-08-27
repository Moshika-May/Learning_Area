# Initial list of tasks
tasks = [
    "Buy groceries", 
    "Clean the house", 
    "Finish the report", 
    "Call Alice", 
    "Pay bills"
]

print("Initial to-do list:")
for task in tasks:
    print(f'  - {task}')

# Insert a new task at a specific position
position = int(input("Enter the position to insert the new task (0-based index): "))
new_task = input("Enter the new task to insert: ")
tasks.insert(position, new_task)

print("\nTo-do list after insertion:")
for task in tasks:
    print(f'  - {task}')

# Sort the tasks alphabetically
tasks.sort()

print("\nTo-do list after sorting:")
for task in tasks:
    print(f'  - {task}')
