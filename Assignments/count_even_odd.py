# 6810742293 Kasidej Mahanin

# Declaring variables sections
loop = 'y'
odd = 0
even = 0

# Compute section
# If ""loop"" values was 'y' then program will do while loop and ask user integer number
# and then consider if-else statement to calculate that number was odd or even and ask user to loop again or not
# If ""loop"" values was 'n' then program will exit loop and print output
# If ""loop"" values wasn't ethier 'y' or 'n' program will ask user to input 'y' or 'n' to consider while loop
while True:
    if loop == 'n':
        break
    number = int(input('Enter a positive integer: '))
    if number % 2 == 0:
        even += 1
    if number % 2 != 0:
        odd += 1
    while True:
        loop = input('Do you want to continue? (y/n): ')
        if loop == 'y':
            break
        if loop == 'n':
            break
        elif loop != 'n' and loop != 'y':
            print('Please enter "y" or "n"')

# Output section
print(f'Even numbers: {even}')
print(f'Odd numbers: {odd}')