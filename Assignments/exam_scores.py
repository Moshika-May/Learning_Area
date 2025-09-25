# 6810742293 Kasidej Mahanin

# Input variable section
# This list will store all valid scores entered by the user
number = [int(input('Enter a score [0-100] (-1 to end): '))]

# Continue asking for scores until user enters -1
# Each valid score (0-100) is added to the list
# Invalid scores (<0 or >100) are rejected with an error message
# The loop ends when -1 is entered
while True:
    if number[-1] == -1:
        break
    
    if number[-1] < 0 or number[-1] > 100:
        print('Error: Invalid score!')
        number.remove(number[-1])
    number.append(int(input('Enter a score [0-100] (-1 to end): ')))

# Calculation section
# Calculate total, count, and average of valid scores
total = sum(number[:-1])
count = len(number) - 1
if count != 0:
    average = total / count

# Output section
# If no valid scores were entered, print a message
# Otherwise, print the list of scores, count, total, and average
if count == 0:
    print('No valid scores were entered.')

if count != 0:
    print(f'Scores: {number[:-1]}')
    print(f'Count: {count}')
    print(f'Total: {total}')
    print(f'Average: {average:.2f}')