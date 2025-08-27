# void functions with a single parameter
def c1(x):
    # x is a parameter
    print(f"In function c1: x = {x}")

def main():
    c1(1)     # argument is 1

    m = 2
    c1(m)     # argument is m

    n = m*m
    c1(n)     # argument is n

    c1(1+m+n) # argument is 1+m+n

main()
