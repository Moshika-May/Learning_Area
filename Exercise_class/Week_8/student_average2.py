NUM_STUDENTS = 3

# students = []
# for num in range(1, NUM_STUDENTS + 1):
#     name = input(f'Input student name #{num}: ')
#     math_score = int(input("Input Math score: "))
#     science_score = int(input("Input Science score: "))
#     students.append((name, math_score, science_score))
# print(f'{students = }')

# students = []
# for num in range(1, NUM_STUDENTS + 1):
    # Alice 85 78
    # Bob 70 82
    # David 65 70
#     data = input(f'Student #{num} (input name, math and science score): ').split()
#     name, math, sci = data[0], int(data[1]), int(data[2])
#     students.append((name, math, sci))
# print(f'{students = }')

students = []
for num in range(1, NUM_STUDENTS + 1):
    # Alice 85 78
    # Bob 70 82
    # David 65 70
    name, math, sci = input(f'Student #{num} (input name, math and science score): ').split()
    students.append((name, int(math), int(sci)))
print(f'{students = }')