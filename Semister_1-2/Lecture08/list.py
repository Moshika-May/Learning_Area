list1 = []
n = int(input("Times to repeat: "))

while len(list1) != n:
    print(list1)
    print(f"Length: {len(list1)}")
    list1.append((input("Enter number to list: ")))

print(list1)