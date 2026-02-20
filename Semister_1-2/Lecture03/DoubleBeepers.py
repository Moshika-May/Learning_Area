from karel.stanfordkarel import *

def main():
    while front_is_clear() and no_beepers_present():    # Move until found beeper
        move()
    while True:
        while beepers_present():        # Checked that beepers was present then pick 1 beepers and turn back and move then put 2 beeper
            pick_beeper()               # Repete until all beepers was move to previous box and lastly move all beepers to original box and move 1 time
            turn_back()
            move()
            put_beeper()
            put_beeper()
            turn_back()
            move()
        turn_back()
        move()
        while beepers_present():
            pick_beeper()
            turn_back()
            move()
            put_beeper()
            turn_back()
            move()
        break
    turn_back()
    while front_is_clear() and no_beepers_present():
        move()
    move()

def turn_back():
    turn_left()
    turn_left()

# don't edit these next two lines
# they tell python to run your main function
if __name__ == '__main__':
    run_karel_program()