from karel.stanfordkarel import *

def main():     # Main logic
    while left_is_clear():      # Check that next row exist
        put_beeper_to_wall()
        reset_position_facing_invert()
        move_to_next_row_and_reset_facing()
    put_beeper_to_wall()

def move_to_next_row_and_reset_facing():        # Move to next row and reset facing
    turn_right()
    move()
    turn_right()

def reset_position_facing_invert():     # Move to left row but not reset facing
    turn_back()
    move_to_wall()

def put_beeper_to_wall():       # Put beepers and until dead end
    while front_is_clear():
        put_beeper()
        move()
    put_beeper()

def move_to_wall():     # Move until dead end
    while front_is_clear():
        move()

def turn_right():
    for i in range(3):
        turn_left()    

def turn_back():
    for i in range(2):
        turn_left()
    

# don't edit these next two lines
# they tell python to run your main function
if __name__ == '__main__':
    run_karel_program()