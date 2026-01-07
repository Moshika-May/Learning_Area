number = int(input('Enter a positive integer: '))

result = "odd"
if number % 2 == 0:
    result = 'even'

print(f'This number "{number}" is {result}')