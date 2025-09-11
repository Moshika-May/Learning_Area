# 6810742293 Kasidej Mahanin
total = 0
count = 0
maximum = 0
minimum = 0

first_num = int(input('Enter a score (-1 to end): '))

if first_num == -1:
    print("No scores entered.")
else:
    # Initialize everything with the first valid number
    count = 1
    total = first_num
    maximum = first_num
    minimum = first_num

    # Now, loop for all other numbers
    while True:
        number = int(input('Enter a score (-1 to end): '))

        # 1. Check for the stop condition FIRST
        if number == -1:
            break  # Exit the loop

        # 2. Check for invalid input
        if number < 0:
            print('Invalid number, please enter a positive number.')
            continue # Skip to the next loop iteration

        # 3. Update the total and count
        total += number
        count += 1

        # 4. Compare to find the new max or min
        if number > maximum:
            maximum = number
        if number < minimum:
            minimum = number

    # This calculation is now done only if numbers were entered
    average = total / count

    print(f'Display counted: {count}')
    print(f'Average score: {average:.2f}')
    print(f'Minimum score: {minimum}')
    print(f'Maximum score: {maximum}')