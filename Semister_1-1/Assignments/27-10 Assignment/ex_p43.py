# Kasidej Mahanin 6810742293

def print_digit(a_string):

    digits_to_find = '0123456789'            # Define values to find
    digits_found = []                        # Empyty list to store found digits
    for char in a_string:                    # Loop to check each character
        if char in digits_to_find:           # If char was digit
            digits_found.append(char)        # Add char that was digit to list
    
    for i in digits_found:                   # Print a digits_found in for loop
        print(i, end=" ")
    print()

def main():

    print_digit('24 hours in 1 day, 7 days in a 1 week.')
    message = 'I met a man with 7 wives. Each wife had 7 sacks.'
    print_digit(message)

main()