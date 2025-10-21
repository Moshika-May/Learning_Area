def fn1(a_list):
    a_list[0] *= 10
    a_list[-1] += 2

def main():
    list1 = [1, 2]
    fn1(list1)
    print(list1)

main()