def stat(data):
    minimum = min(data)
    maximum = max(data)
    mean = sum(data) / len(data)
    return minimum, maximum, mean

def main():
    input_list = input("Enter data: ").split()
    data = []
    for item in input_list:
        data.append(float(item))

    res = stat(data)
    print(f"result = {res}")
    print(f"min = {res[0]}, max = {res[1]}, mean = {res[2]}")

main()
