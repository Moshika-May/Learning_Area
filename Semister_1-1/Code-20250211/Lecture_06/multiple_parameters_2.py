# void functions with multiple parameters
def d2(x, y):
    # x and y are parameters
    print(f"{x} + {y} => {x + y}")

def main():
    d2(1, True)       # arguments are 1 and True

    m = 3.14159
    d2(m, 5)          # arguments are m and 5

    m = 1
    d2((m+1)*2, 2*m)  # arguments are (m+1)*2 and 2*m

main()
