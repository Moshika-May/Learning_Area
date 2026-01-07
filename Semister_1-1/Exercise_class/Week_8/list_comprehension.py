numbers = [4, 2, 6, 2, 5]
list1 = []
for num in numbers:
    if num > 2:
        list1.append(num * 2)
print(f'{list1 = }')

print()
list2 = [num * 2 for num in numbers if num > 2]
print(f'{list2 = }')