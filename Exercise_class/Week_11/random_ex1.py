import random

def main():
    numbers = []
    for count in range(5):
        numbers.append(random.randint(1, 100))
    print(numbers)

main()