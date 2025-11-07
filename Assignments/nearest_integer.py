# 6810742293 Kasidej Mahanin

from math import floor, ceil

def checking(x):
    x_floor = floor(x)
    x_ceil = ceil(x)

    if x - x_floor == 0.5:
        print(f'{x_floor} - {x} - {x_ceil}')
    elif x - x_floor > 0.5:
        print(f'{x} -> {x_ceil}')
    else:
        print(f'{x_floor} <- {x}')

def main():
    number = float(input('Type a number: '))
    checking(number)

main()