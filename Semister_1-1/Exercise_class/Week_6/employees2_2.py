# List of employee names
employees = ["Alice", "Bob", "Peter"]
print(f"List of employees: {employees}")

# User input for the name to search and the new name
old_name = input("Enter the name of the employee to replace: ")
new_name = input("Enter the new name: ")

# Searching for the name and replacing it
if old_name in employees:
    index_old_name = employees.index(old_name)
    employees[index_old_name] = new_name
    print(f"Updated list of employees: {employees}")    # Display the updated list of employees
else:
    print(f'{old_name} is not in employees')

#for index in range(len(employees)):
#    if employees[index] == old_name:
#        employees[index] = new_name
#        break

