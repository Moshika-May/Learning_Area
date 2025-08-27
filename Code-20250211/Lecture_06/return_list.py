# zero out all values below a given threshold in a list
def zero_below(a_list, threshold):
    res = a_list[:]  # create a new list from a_list
    for i in range(len(a_list)):
        if res[i] < threshold:
            res[i] = 0
    return res

def main():
    data = [10 , 20, 30, 40, 50, 60, 70, 80, 90, 100]
    print(f"Before: {data}")
    res = zero_below(data, 50)
    print(f"After: {data}")
    print(f"After: {res}")

main()