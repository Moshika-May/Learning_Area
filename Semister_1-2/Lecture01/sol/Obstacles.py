from karel.stanfordkarel import *

def main():
    # Karel starts facing East in the bottom left corner of the world and ends facing East in the bottom right corner of the world.
    move()
    jump_up()
    jump_up()
    jump_up()
    move()
    move()

def turn_right():
    turn_left()
    turn_left()
    turn_left() 

def jump_up():
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()
    put_beeper()


# There is no need to edit code beyond this point
if __name__ == '__main__':
    run_karel_program()