def main():
    # Initialize an accumulator variable
    count = 0
    
    # Get a string from the user.
    my_string = input('Enter a sentence: ')

    # Count the Ts.
    for ch in my_string:
        if ch == 'T' or ch  == 't':
            count += 1

    # Print the result.
    print('The letter T appears', count, 'times.')

main()
