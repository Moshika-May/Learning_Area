# void functions with a single parameter
def c3(x):
    # x is a parameter
    y = len(x)
    print(f"Length is => {y}")

def main():
    c3("Message") # argument is "Message"

    m = [1,2,3]
    c3(m)         # argument is m

    n = (4,5,6,7)
    c3(n)         # argument is n

main()
