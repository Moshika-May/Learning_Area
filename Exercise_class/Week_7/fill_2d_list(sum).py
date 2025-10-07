# Constants for rows and columns
ROWS = 3
COLS = 4
# Create a two-dimensional list.
values = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]
# Fill the list with numbers.
i = 1
for r in range(ROWS):
    for c in range(COLS):
        values[r][c] = i
        i += 1

total = 0
number = []
for sublist in values:
#     total += sum(sublist)
    for num in sublist:
        number.append(num)

total = sum(number)
# Display the numbers.
print(values)
print(total)
# print(sum(sum(values, [])))