import math

def checking(x):
    x_floor = math.floor(x)
    x_ceil = math.ceil(x)
    if x > x_floor:
        print(f'{x} -> {x_ceil}')
    elif x < x_floor:
        print(f'{x} <- {x_ceil}')
    elif x > x_ceil:
        print(f'{x} -> {x_floor}')
    elif x < x_ceil:
        print(f'{x} <- {x_floor}')

def main():
    number = float(input('Type a number: '))
    checking(number)

main()