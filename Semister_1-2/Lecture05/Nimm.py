def main():
    stone_in_total = 20

    while True:
        for i in range(1, 3):
            if stone_in_total == 0:
                print(f'Player {i} wins!')
                return

            print(f'There are {stone_in_total} stones left')
            stones_remove = int(input(f'Player {i} Would you like to remove 1 or 2 stones? '))
            while stones_remove > 2 or stones_remove < 1:
                stones_remove = int(input('Please enter 1 or 2: '))

            stone_in_total -= stones_remove
            print()

if __name__ == '__main__':
    main()