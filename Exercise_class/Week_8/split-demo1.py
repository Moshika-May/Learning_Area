numbers = input('Input 5 numbers: ').split()
print(f'{numbers = }')

numbers2 = []
for num_string in numbers:
    numbers2.append(int(num_string))
print(f'{numbers2 = }')

numbers3 = [int(num_string) for num_string in numbers]
print(f'{numbers3 = }')