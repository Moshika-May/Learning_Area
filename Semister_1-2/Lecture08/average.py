def average(list):
    return sum(list) / len(list)

def main():
    list = [1, -2, 4, -4, 9, -6, 16, -8, 25, -10]
    average(list)
    print(average(list))

if __name__ == "__main__":
    main()