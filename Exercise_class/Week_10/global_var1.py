b = 2                   # Global variable
PI = 3.141              # Global Constant

def fn1():
    global b
    b += 20
    print(f'fn1: {b = }')


def fn2():
    global b
    b = 30
    print(f'fn2: {b = }')


def main():
    global b
    b = 100
    fn1()
    fn2()
    b = 10              # Local variable
    print(f'main: {b = }')


main()
# Better avoid global variable