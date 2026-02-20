from karel.stanfordkarel import *

def main():
    move()
    pick_beeper_10()
    move()
    pick_beeper_10()
    move()
    pick_beeper_10()

def pick_beeper_10():
    for i in range(10):
        pick_beeper()
    move()

# don't edit these next two lines
# they tell python to run your main function
if __name__ == '__main__':
    run_karel_program()