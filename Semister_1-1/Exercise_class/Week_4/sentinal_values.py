total = 0
count = 0

number = int(input('Enter a number (-1 to end): '))
while number < -1 or number > 10:
    print('Invalid input. Please enter a number between 0 and 10, or -1 to end.')
    number = int(input('Enter a number (-1 to end): '))

while number != -1:
    count += 1
    total += number
    number = int(input('Enter a number (-1 to end): '))
    while number < -1 or number > 10:
        print('Invalid input. Please enter a number between 0 and 10, or -1 to end.')
        number = int(input('Enter a number (-1 to end): '))

average = total / count

print(f'{total = }')
print(f'{average = :.2f}')