# variable can only be accessed after it is defined
def a2():
    x = 10
    # can use variable x after it is defined
    print(f"In function a2: x = {x}")

def b2():
    # this will cause an error because variable x is not defined yet
    # take note of the error message
    print(f"In function b2: x = {x}")
    x = 20

def main():
    a2()
    b2() # this function call will cause an error

main()
