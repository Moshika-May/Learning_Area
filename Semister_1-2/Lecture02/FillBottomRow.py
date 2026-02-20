from karel.stanfordkarel import *

def main():
    put_beeper()
    while front_is_clear():
        move()
        put_beeper()


# don't edit these next two lines
# they tell python to run your main function
if __name__ == '__main__':
    run_karel_program()