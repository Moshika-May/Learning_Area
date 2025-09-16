# List of employee names
employees = ["Alice", "Bob"]
print(f"List of employees: {employees}")

# User input for a new employee
new_employee = input("Enter the name of the new employee: ")

# Adding the new employee using concatenation
employees = employees + [new_employee]

# Display the updated list of employees
print("List of employees after adding a new one:")
for index in range(0, len(employees)):
    print(f"{index + 1}. {employees[index]}")
