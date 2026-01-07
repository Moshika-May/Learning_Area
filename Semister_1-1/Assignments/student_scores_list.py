# 6810742293 Kasidej Mahanin

# Input section
# Ask the user for the number of students
# For each student, ask for the number of test scores
# Then, ask for each test score and store them in a list until all scores for that student are entered
num_students = int(input("How many students do you have? "))
for student in range(1, num_students + 1):
    scores = []
    print(f"Student number {student}")
    num_test_scores = int(input(f"How many test for student {student}? "))
    print("-----------------")

    for test_num in range(1, num_test_scores + 1):
        print(f"Test number {test_num}: ", end="")
        score = float(input())
        scores.append(score)

    # Calculation section
    average = sum(scores) / len(scores)

    # Output section
    print(f"The average for student number {student} is: {average:.1f}")
    print()