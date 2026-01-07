# Kasidej Mahanin 6810742293

def print_even(a_list):

    even_numbers = []                           # Empty list to store even numbers
    for num in a_list:                          # Loop to check each number
        if num % 2 == 0:                        # If number is even
            even_numbers.append(num)            # Add even number to list

    for i in even_numbers:                      # Print a even_numbers in for loop
        print(i, end=" ")
    print()

def main():

    print_even([1, 2, 3, 4, 5])
    list_1 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 20, 21, 20]
    list_2 = list(range(20, 0, -3))
    print_even(list_1)
    print_even(list_2)

main()