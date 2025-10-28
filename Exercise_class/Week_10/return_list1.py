def fn1(a_list):
#     list1 = []
#     for num in a_list:
#         list1.append(num * 10)
#    return [num * 10 for num in a_list]


    for i in range(len(a_list)):
        a_list[i] *= 10
    return a_list


def main():
    list1 = [1, 2, 3, 4]
    result = fn1(list1)
#     list2 = fn1(list1)
#     print(list2)
    print(list1)
    print(f'{result = }')

main()