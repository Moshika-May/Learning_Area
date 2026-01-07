# 6810742293 Kasidej Mahanin

# Declaring variables sections
# These variables are used to control the loop and count odd/even numbers
loop = 'y'      # User’s choice to continue or not
odd = 0         # Counter for odd numbers
even = 0        # Counter for even numbers

# Main while-loop section
# Continues running until user decides to stop (loop == 'n')
# Each iteration asks user to enter a positive integer
# Number is classified as even or odd and counters are updated
while True:
    if loop == 'n':     # Exit condition
        break

    # User inputs number
    number = int(input('Enter a positive integer: '))

    # Check if number is even or odd
    if number % 2 == 0:
        even += 1
    if number % 2 != 0:
        odd += 1
    
    # Sub-loop for user confirmation
    # Ask if the user wants to continue (y/n)
    # Loop repeats until valid input is given
    while True:
        loop = input('Do you want to continue? (y/n): ')
        if loop == 'y':
            break
        if loop == 'n':
            break
        elif loop != 'n' and loop != 'y':
            print('Please enter "y" or "n"')

# Output section
# After user ends program, print total counts of even and odd numbers
print(f'Even numbers: {even}')
print(f'Odd numbers: {odd}')