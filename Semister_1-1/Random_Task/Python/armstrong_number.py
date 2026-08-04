def armstrong_numbers(n):
    if n <= 0:
        return
    if n == 1:
        start = 0
    else:
        start = 10 ** (n - 1)

    end = 10 ** n
    results = []

    for num in range(start, end):
        temp = num
        total_sum = 0
        while temp > 0:
            digit = temp % 10       # 153 % 10 = 3
            total_sum = total_sum + (digit ** n)
            temp = temp // 10       # 153 // 10 = 15

        if total_sum == num:
            results.append(str(num))

    if len(results) > 0:
        print(" ".join(results))

def main():
    armstrong_numbers(3)

if __name__ == "__main__":
    main()