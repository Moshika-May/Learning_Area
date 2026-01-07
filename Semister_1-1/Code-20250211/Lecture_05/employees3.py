employees = ["Alice", "Bob", "Peter"]
print(f"List of employees: {employees}")

# User input for the name to search and remove
name_to_remove = input("Enter the name of the employee to remove: ")

# Searching for the name and removing it
for index in range(len(employees)):
    if employees[index] == name_to_remove:
        employees = employees[:index] + employees[index+1:]
        break

# Display the updated list of employees
print(f"Updated list of employees: {employees}")