# each function has its own local variable "x"
def a1():
    # a local variable "x" in function a1()
    x = 10
    print(f"In function a1: x = {x}")
def b1():
    # another local variable "x" in function b1()
    x = 20
    print(f"In function b1: x = {x}")
def main():
    a1()
    b1()
    a1()
    b1()
main()
