# NUM_EMPLOYEES is used as a constant for the size of the list.
NUM_EMPLOYEES = 6

# Create a list to hold employee hours.
hours = []

# Get each employee's hours worked.
for index in range(NUM_EMPLOYEES):
    prompt = f'Enter the hours worked by employee {index + 1}: '
    hours.append(float(input(prompt)))

# Get the hourly pay rate.
pay_rate = float(input('Enter the hourly pay rate: '))

# Display each employee's gross pay.
for index in range(NUM_EMPLOYEES):
    gross_pay = hours[index] * pay_rate
    print(f'Gross pay for employee {index + 1}: ${gross_pay:,.2f}')

maximum = max(hours) * pay_rate
minimum = min(hours) * pay_rate
maximum_index = hours.index(max(hours)) + 1
minimum_index = hours.index(min(hours)) + 1

print(f'Employee {maximum_index} gets maximum gross pay ${maximum:.2f}')
print(f'Employee {minimum_index} gets minimum gross pay ${minimum:.2f}')
