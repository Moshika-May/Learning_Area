# void functions with a single parameter
def c2(x):
    # x is a parameter
    print(f"In function c2: x = {x}")

def main():
    c2([1,2,3])  # argument is [1,2,3]

    m = [4,5,6,7]
    c2(m)        # argument is m

    n = (7,8,9,10,11)
    c2(n)        # argument is n

main()
