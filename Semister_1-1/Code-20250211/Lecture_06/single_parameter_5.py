# void functions with a single parameter
def c5(x):
    # y is a parameter
    y = sorted(x)
    print(f"Min = {y[0]}, May = {y[-1]}, Length is => {len(y)}")

def main():
    c5([1, 3, 5, 7, 3, 5, 1])

    c5([2020, -5, -10, 8, 12])

    m = (3.5, 1.5, -2.7, -9, 11, 20.2)

    c5(m)

main()
