def contains_twice(str, str_twice):
    n = 0
    for i in range(len(str)):
        if str_twice == str[i]:
            n += 1
        if n == 2:
            return True
    return False

def main():
    print(contains_twice("hello", 'l'))

if __name__ == "__main__":
    main()