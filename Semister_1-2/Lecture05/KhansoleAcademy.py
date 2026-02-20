import random

def main():
    int1 = random.randint(10, 99)
    int2 = random.randint(10, 99)
    int_answer = int1 + int2

    print("Khansole Academy")
    print(f'What is {int1} + {int2}?')  
    int_user_answer = int(input("Your answer: "))

    if int_answer == int_user_answer:
        print('Correct!')

    else:
        print('Incorrect.')
        print(f'The expected answer is {int_answer}')
    
if __name__ == '__main__':
    main()