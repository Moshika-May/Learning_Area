def fn1(x, y = "Not Found", z = [1, 2]):        # Default values = 10
    print(f'{x = }, {y = }, {z = }')

def main():
    a, b = 1, 7

    # Sending values = 1, This will overwrite defaut values
    fn1(a)

main()