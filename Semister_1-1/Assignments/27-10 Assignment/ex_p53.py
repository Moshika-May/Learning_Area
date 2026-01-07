# Kasidej Mahanin 6810742293

def print_less(x, a_list):

    less_than_number = []                           # Empty list to store less than x numbers
    for less in a_list:                             # Loop to check each number
        if less < x:                                # If number was less than x
            less_than_number.append(int(less))      # Add less number to list

    for i in less_than_number:                      # Print a less_than_number in for loop
        print(i, end=" ")
    print()

def main():

    print_less(50, [50, 51, 99, 79, 47, 83, 90, 39, 90, 25])
    a, list_1 = 55, list(range(30, 100, 15))
    print_less(a, list_1)

main()