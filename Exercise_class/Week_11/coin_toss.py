# This program simulates 10 tosses of a coin.
from random import seed, randint, random
seed(1)
# Constants
HEADS = 1
TAILS = 2
TOSSES = 10

def main():
    for toss in range(TOSSES):
        # Simulate the coin toss.
        if randint(HEADS, TAILS) == HEADS:
            print('Heads')
        else:
            print('Tails')
            
# Call the main function.
main()
