total = 0
for i in range(3):
    total = 0
    for j in range(1, 6):
        print(j, end=' ')
        total += j
    print()
print(f'The total is {total}.')