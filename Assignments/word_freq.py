# 6810742293 Kasidej Mahanin

# Declaring variables section
# Declaring empty list
words = []
counts = []

# Input looped until find word "END"
while True:
    word = input('Enter word (END to stop): ')

    # If found word END, program will break from loop  
    if word == 'END':
        break
    # if found same word, will top up same word count
    if word in words:
        index = words.index(word)
        counts[index] += 1
    # else new word found
    else:
        words.append(word)
        counts.append(1)

# Output all word in list
print(f"Words : {words}")

# Display counts
print("Counts: [", end='')
if len(counts) > 0:
    for i in range(len(counts) - 1):
        print(f'{counts[i]: >3}', end=' ,')
    
    print(f'{counts[-1]: >3}', end='')
print(" ]")

# Display Most frequent
if len(counts) > 0:
    max_count = max(counts)
    max_index = counts.index(max_count)
    most_frequent_word = words[max_index]
    print(f"Most frequent: '{most_frequent_word}' ({max_count})")