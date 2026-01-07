# 6810742293 Kasidej Mahanin

# Declaring variables section
# Declaring empty list
classes_amount = []
classes_name = []
scores = []

# Declaring prefix value
highest_average = -1.0
highest_classes_name = ""

# Input validation of n class
classes_amount.append(int(input('Enter number of classes: ')))
while classes_amount[-1] < 1:
    del classes_amount[-1]
    print(f'Error: invalid number of classes(number of classes must be more than 1)')
    classes_amount.append(int(input('Enter number of classes: ')))

# Looping program n times
# To ask Class name
# To find index to slicing a scores list (for calculation)
for i in range(classes_amount[-1]):
    print()
    classes_name.append(input('Class name: '))
    start_index = len(scores)

    # Input scores to list validation
    scores.append(float(input('Enter score(-1 to stop): ')))
    while scores[-1] < -1:      # Validating that user input right value
        del scores[-1]          # Delete any recent value that user input
        print(f"Error: score can't be any negative number")
        scores.append(float(input('Enter possitive score(-1 to stop): ')))

    # Input other scores to list validation
    while scores[-1] != -1:     # Decide to terminate input other scores
        scores.append(float(input('Enter score(-1 to stop): ')))
        while scores[-1] < -1:
            del scores[-1]
            print(f"Error: score can't be any negative number")
            scores.append(float(input('Enter possitive score(-1 to stop): ')))

    # Prefix value before calculation
    del scores[scores.index(-1)]            # Delete -1 in list
    current_score = scores[start_index:]    # Slicing scores to calculate

    # If theres was any score in list, will be True
    # Calculate average score
    # Print class name and average after ended input scores in n classes
    if current_score:
        average_scores = sum(current_score) / len(current_score)
        print(f'{classes_name[-1]} average = {average_scores:.2f}')

        # Check and set new highest average in n classes
        if average_scores > highest_average:
            highest_average = average_scores
            highest_classes_name = classes_name[-1]
    
    # If no scores input print prompt
    else:
        print(f'{classes_name[-1]} average = 0.00')

# Validation that there was enough scores to print highest average
print()
if len(scores) >= 1:
    print(f'Highest average class: {highest_classes_name} ({highest_average:.2f})')