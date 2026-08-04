r = int(input('Enter the range: '))
a = [0] * r
for i in range(r):
    a[i] = (int(input(f'Enter number {i+1}: ')))
print(a)