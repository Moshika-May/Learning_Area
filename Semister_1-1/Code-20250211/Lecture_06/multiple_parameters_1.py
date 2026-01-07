# void functions with multiple parameters
def d1(x, y):
    # x and y are parameters
    print(f"{x} + {y} => {x + y}")

def main():
    d1(1, 2)      # arguments are 1 and 2

    m = 3
    n = 4
    d1(m, n)      # arguments are m and n

    d1(m*m, n*n)  # arguments are m*m and n*n

main()
