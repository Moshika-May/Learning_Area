MAX_NUM = 5

def factorial(n):
    result = 1
    for i in range(1, n + 1,):
        result *= i

    return result
def main():
    for i in range(MAX_NUM):
        print(f"factorial({i}): {factorial(i)}")
if __name__ == "__main__":
    main()