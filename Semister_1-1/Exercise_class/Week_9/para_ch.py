def fn1(x, y):
    x += 1
    y += 2
    print(f'{x = }, {y = }')

def main():
    a, b = 5, 10
    fn1(a ,b)
    print(f'{a = }, {b = }')

main()