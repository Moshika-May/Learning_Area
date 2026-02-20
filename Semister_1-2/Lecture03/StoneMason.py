from karel.stanfordkarel import *

def main():
    while front_is_clear():     # Checking that front is clear before ready to move to next col
        place_beeper_for_1_col()
        move_to_designated()
    place_beeper_for_1_col()

def place_beeper_for_1_col():       # Place beeper in current col
    turn_left()
    put_beeper_to_wall()
    turn_back()
    move_to_wall()
    turn_left()
    # This will turn left and place beepers until dead end and then reset position and facing
    
def move_to_designated():       # Move to designated position
    for i in range(4):      # Move 4 times
        if front_is_clear():    # Always check that its moveable
            move()

def turn_back():
    for i in range(2):
        turn_left()

def move_to_wall():     # While fornt is clear move to dead end
    while front_is_clear():
        move()

def put_beeper_to_wall():       # While front is clear place beeper and move to next box
    while front_is_clear():     # Always check that front is clear to avoid errors
        put_beeper()
        move()
    put_beeper()


# don't edit these next two lines
# they tell python to run your main function
if __name__ == '__main__':
    run_karel_program()