keep_going = 'y'

while keep_going == 'y' or keep_going == 'Y':
    start = int(input('Enter the starting number: '))
    end = int(input('Enter the ending number: '))
    if start > 0 and end > 0 and start < end + 1:
        print('_' * 30, end='\n\n')
        print(f'{'Number':>13s}{'Square':>11s}')
        print('_' * 30, end='\n\n')
        for num in range(start, end + 1):
            square = num ** 2
            print(f'{num:10d} {square:10d}')
        print('_' * 30)
    else:
        print('Invalid input.')
    keep_going = input('Do you want to continue? (Y/N): ')