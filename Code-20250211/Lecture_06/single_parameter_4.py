# void functions with a single parameter
def c4(x):
    # x is a parameter
    y = len(x)  # x must have value that can be used with function len
    print(f"Length is => {y}")

def main():
    c4(1)      # argument is 1, this function call will cause an error

    m = True
    c4(m)      # argument is m, this function call will cause an error

    n = 3.14159
    c4(n)      # argument is n, this function call will cause an error

main()
