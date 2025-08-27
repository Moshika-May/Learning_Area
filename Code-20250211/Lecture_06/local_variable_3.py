# a function can define any number of local variables
def a3():
    x = 10        # define a local variable x
    print(f"In function a3: x = {x}")

    y = 4.5       # define another local variable y
    print(f"In function a3: y = {y}")

    z = [1,2,3]   # define another local variable z
    print(f"In function a3: z = {z}")

def main():
    a3()

main()
