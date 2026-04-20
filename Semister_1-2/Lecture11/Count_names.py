def main():
    name_dic = {}
    while True:
        name = input("Enter name: ")
        if name == "":
            break

        elif name not in name_dic:
            name_dic[name] = 1

        elif name in name_dic:
            name_dic[name] += 1

        else:
            print(f'Error')

    for name in name_dic:
        value = name_dic[name]
        print(f'Entry [{name}] has count {value}')

if __name__ == "__main__":
    main()