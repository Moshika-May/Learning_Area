list1 = ['A', 'B', 'C']

# for i in range(len(list1)):
#     print(f"{i+1}.{list1[i]}")

for i, ch in enumerate(list1, start=1):
    print(f"{i}.{ch}")