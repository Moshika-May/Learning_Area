# List of employees where each employee is represented as a tuple.
# (Employee ID, Employee Name, Email Address, Phone Number)
employees = [
    (1, "Alice", "alice@example.com", "123-456-7890"),
    (2, "Bob", "bob@example.com", "987-654-3210"),
    (3, "Charlie", "charlie@example.com", "555-123-4567"),
    (4, "David", "david@example.com", "444-555-6666"),
    (5, "Eve", "eve@example.com", "111-222-3333")
]

# Define the partial name to search for
search_name = input("Enter the partial name of the employee: ")

# Define what to search for (phone or email)
search_type = input("Do you want to search for 'phone' or 'email'? ")

if search_type == "phone":
    results = [
        (employee[1], employee[3])
        for employee in employees
        if search_name in employee[1]
    ]
    result_type = "Phone number"
elif search_type == "email":
    results = [
        (employee[1], employee[2])
        for employee in employees
        if search_name in employee[1]
    ]
    result_type = "Email address"
else:
    print("Invalid search type. Please choose 'phone' or 'email'.")
    results = []
    result_type = ""

# Print the results
if results:
    for name, contact in results:
        print(f"{result_type} of {name}: {contact}")
else:
    print(f"No employee found with the partial name '{search_name}'")
