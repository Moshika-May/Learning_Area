# 6810742293 Kasidej Mahanin

# Declaring variables
total = 0
count = 0

# Input number
number = int(input(f'Enter a score (-1 to end): '))

# If ""number"" was more than -1, Will assign maximum(to set maximum to temp state), minimum(to set minimum to temp state), count, total then break
# If ""number"" was -1, Will break and also will break on next while loop as well also count will be 0 that will use in last output part
# If ""number"" was not -1 and lower than -1, Will print "invalid number" then ask user to input again until it was positive number or -1
while True:
    if number == -1:
        break
    elif number > -1:
        maximum = number
        minimum = number
        count += 1
        total += number
        break
    else:
        print('Invalid number, please enter positive number')
        number = int(input(f'Enter a score (-1 to end): '))

# This was next step from first while loop
# The ""number"" variable was same value and will consider in if-else statement that ""number"" value was -1 or not.
# If ""number"" was -1, Will break loop before asking user input and proceed to next if statement.
# If ""number"" was positive number program will ask user to input again to add more ""count"" and top up total value
# and then will consider that new number that user input was new maximum(if higher number this will replace maximum)
# or minimum(if lower number this will replace minimum).
# If ""number"" was negative number, Wil print "invalid number" and than loop to ask user to input again until user input was -1.
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

# This will check that program how to end program.
# If program has count > 0, Thats mean program was active second while and had to calculate ""average"" then print output.
# If program has count <= 0, Thats mean program wasn't active second loop so will print "no score entered." cause ""number"" was -1 so exit program.
if count > 0:
    average = total / count
    print(f'Average score: {average:.1f}')
    print(f'Minimum score: {minimum:.1f}')
    print(f'Maximum score: {maximum:.1f}')
else:
    print('No scores entered.')