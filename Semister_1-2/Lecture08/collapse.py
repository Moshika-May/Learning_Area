def collapse(a):
    num = []
    for i in range(0, len(a), 2):
        if i + 1 < len(a):
            num.append(a[i] + a[i + 1])
        else:
            num.append(a[i])

    return num

def main():
    list_a = [7, 2, 8, 9, 4, 13, 7, 1, 9, 10]
    print(f'Result: {collapse(list_a)}')

if __name__ == "__main__":
    main()