def fn1(x = 10, y = 20, z = 30):
    print(f'{x = }, {y = }, {z = }')

def main():
    a, b = 1, 3
    fn1(y = b, x = a + b)

    #  vvvvvv vvvvvv This is keyword arg
#     fn1(x = a, y = b)

main()