# void functions with multiple parameters
def d4(x, y):
    # x and y are parameters
    print(f"{x} + {y} => {x + y}")

def main():
    m = [1, 2]
    n = [3, 4, 5]
    d4(m, n)            # arguments are m and n

    d4(len(m), len(n))  # arguments are len(m) and len(n)

    d4(min(m), max(n))  # arguments are min(m) and max(n)

main()
