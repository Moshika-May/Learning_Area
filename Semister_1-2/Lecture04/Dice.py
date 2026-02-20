import random

def main():
    dice_face = int(input("How many sides does your dice have? "))
    user_roll = random.randint(1, dice_face)
    print(f'Your roll is {user_roll}')

if __name__ == '__main__':
    main()