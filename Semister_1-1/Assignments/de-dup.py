# 6810742293 Kasidej Mahanin

# Declaring empty list
all_items = []
unique_items = []

# Loop input until found END
while True:
    word = input('Enter word (END to stop): ')

    # If found word END, break from loop
    if word == 'END':
        break

    all_items.append(word)      # Add new word to list

    # Check if these word are same in list or not
    if word not in unique_items:
        unique_items.append(word)   # If not added it in list

# Display result
print(f"Before: {len(all_items)} items")
print(f"After : {len(unique_items)} items")
print(f"Unique: {unique_items}")