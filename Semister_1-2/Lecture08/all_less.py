def all_less(list_a, list_b):
    if len(list_a) != len(list_b):
        return False
    len_list = len(list_a)

    for i in range(len_list):
        index_a = list_a[i]
        index_b = list_b[i]
        if index_a >= index_b:
            return False

    return True

def main():
    list_a = [45, 20, 300]
    list_b = [50, 41, 600]
    print(all_less(list_a, list_b))

if __name__ == "__main__":
    main()