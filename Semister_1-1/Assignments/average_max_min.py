# 6810742293 Kasidej Mahanin

# Declaring variables section
# These variables will be used to keep track of totals, counts
total = 0
count = 0

# First input section
# Program asks for the first score. This is important to initialize min/max values.
number = int(input(f'Enter a score (-1 to end): '))

# First while-loop section
# Validate the first input
# If first number is valid (>=0), initialize maximum and minimum with it
# If input is -1, exit immediately (no scores entered)
# If input is less than -1, show error and re-ask until user enters >=0 or -1
while True:
    if number == -1:        # Exit immediately if no scores are to be entered
        break
    elif number > -1:       # Valid first number → initialize min and max
        maximum = number
        minimum = number
        count += 1
        total += number
        break
    else:                   # Invalid input (< -1)
        print('Invalid number, please enter positive number')
        number = int(input(f'Enter a score (-1 to end): '))

# Second while-loop section
# Continue asking for scores until user enters -1
# Each valid score (>=0) is added to total, count, and checked for min/max
# Negative numbers (< -1) are invalid, error message shown, and user is asked again
while True:
    if number == -1:
        break
    number = int(input(f'Enter a score (-1 to end): '))
    if number > -1:
        count += 1
        total += number
        if number > maximum:
            maximum = number
        if number < minimum:
            minimum = number
    elif number < -1:
        print('Invalid number, please enter positive number')

# Output section
# If at least one valid score was entered, calculate and print average, min, and max
# If no scores were entered (count == 0), print "No scores entered."
if count > 0:
    average = total / count
    print(f'Average score: {average:,.1f}')
    print(f'Minimum score: {minimum:,.1f}')
    print(f'Maximum score: {maximum:,.1f}')
else:
    print('No scores entered.')