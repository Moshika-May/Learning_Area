total = 0
list1 = [1, 2, 3, 4, 5, 6]

for i in range(len(list1)):
    list1[i] *= 2
    total += list1[i]

print(list1)
print(total)

print('==========================', end='\n\n')
list4 = [1,2,3]
list5 = [4,5,6]

print()

# i = 0
# while i < len(list1):
#     print(list1[i], end=' ')
#     i += 1
# print()


# for i in range(0, len(list1), 2):
#     print(list1[i], end=' ')
# print()