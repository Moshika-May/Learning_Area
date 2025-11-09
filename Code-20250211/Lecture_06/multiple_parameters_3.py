 # void functions with multiple parameters
def d3(x, y):
    # x and y are parameters
    print(f"{x} + {y} => {x + y}")

def main():
    d3([1, 2], [3, 4, 5])  # arguments are [1, 2] and [3, 4, 5]

    m = [6, 7]
    n = [8, 9, 10]
    d3(m, n)    # arguments are m and n

    d3(n, m)    # arguments are n and m (note the order of n and m)

main()
