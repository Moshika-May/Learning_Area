def fn1(a_list):
    print(id(a_list))
    a_list = a_list.copy()
    print(id(a_list))
    a_list[0] *= 10
    a_list[1] *= 2

    print(f'{a_list = }')

def main():

    list1 = [1, 2]              # Mutable object
    print(id(list1))
    fn1(list1)
    print(f'{list1 = }')

main()