def plus(num1, num2):
    result = num1 + num2
    print(f'{num1} + {num2} = {num1 + num2}')

def main():
    num1, num2 = input('Input 2 numbers: ').split()
    num1 = int(num1)
    num2 = int(num2)
    plus(num1, num2)

main()