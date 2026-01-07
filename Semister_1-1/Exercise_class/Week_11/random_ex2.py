from random import randint, random

def main():
    numbers = []
    for count in range(randint(1, 5)):
        numbers.append(randint(1, 100))
        numbers.append(random())
    print(numbers)

main()