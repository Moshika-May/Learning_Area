# The NUM_DAYS constant holds the number of
# days that we will gather sales data for.
NUM_DAYS = 5

# Create a list to hold the sales
# for each day.
sales = [0] * NUM_DAYS  # [0, 0, 0, 0, 0]

# Create a variable to hold an index.
index = 0

print('Enter the sales for each day.')

# Get the sales for each day.
while index < NUM_DAYS:     # 0 < 5
    sales[index] = float(input(f'Day #{index + 1}: '))
    index += 1
    print(sales)

# Display the values entered.
print('Here are the values you entered:')
for value in sales:
    print(value)

first_last = sales[0] + sales[-1]
print(first_last)