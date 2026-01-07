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
        
# Display the numbers.
print(values)
