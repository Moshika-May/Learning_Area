# Data structure containing departments and their employees
departments = [
    [("Alice", 28), ("Bob", 34)],       # HR Department
    [("Charlie", 32), ("David", 25)],   # IT Department
    [("Eve", 29), ("Frank", 38)]        # Finance Department
]

# Nested list comprehension to get employee names above 30
employee_names_above_30 = [
    name
    for department in departments
    for name, age in department
    if age > 30
]

# Print the result
print("Employees above 30 years old:", employee_names_above_30)
