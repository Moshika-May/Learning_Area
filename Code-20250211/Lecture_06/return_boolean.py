def is_even(number):
    # Determine whether number is even.
    # If it is, set status to true.
    # Otherwise, set status to false.
    if (number % 2) == 0:
        status = True
    else:
        status = False
    # Return the value of the status variable.
    return status

def main():
    x = 10
    y = 25
    print(f"{x} is even: {is_even(x)}")
    print(f"{y} is even: {is_even(y)}")

main()
