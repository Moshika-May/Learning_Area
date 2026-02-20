from karel.stanfordkarel import *

# File: shelter.py
# -----------------------------
# The warmup program defines a "main"
# function which should make Karel 
# move to the beeper, pick it up, and
# return home.
def main():
    go_to_beeper()
    pick_beeper()
    return_home()
    
def turn_right():
    turn_left()
    turn_left()
    turn_left()

def turn_around():
    turn_left()
    turn_left()

def go_to_beeper():
    move()
    move()
    turn_right()
    move()
    turn_left()
    move()

def return_home():
    turn_around()
    move()
    turn_right()
    move()
    turn_left()
    move()
    move()
    turn_around()
    
# don't edit these next two lines
# they tell python to run your main function
if __name__ == '__main__':
    run_karel_program()