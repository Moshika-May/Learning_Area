# Kasidej Mahanin 6810742293

def print_square(x, y):

    number_sq_x = pow(x, 2)                                 # Use number x and power by 2
    number_sq_y = pow(y, 2)                                 # Use number y and power by 2
    sum_num_sq = number_sq_x + number_sq_y                  # Sum of power x and y
    
    print(f'{number_sq_x} + {number_sq_y} = {sum_num_sq}')  # Print output

def main():

    print_square(3, 4)
    a, b = 7, 9
    print_square(a, b)

main()