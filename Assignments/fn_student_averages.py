


def calculate_averages(students):
    average = []
    for student in students:
        average = (math_score + science_score) / 2
    return average

def get_students_above_threshold(averages, threshold=75):
    above_threshold = []
    
    return above_threshold

def get_highest_average_student(averages):
    ...

def print_report(averages, above_threshold, highest):
    ...

def main():
    students = []
    name, math_score, science_score = input(f'Student #{student} (input name, math and science score): ').split()
    students.append((name, int(math_score), int(science_score)))



# Calculate the average score of each student.

# Create a list of students who have an average score above 75.
above_75_students = [
    name
    for name, average in student_averages
    if average > 75
]

# Find the student with the highest average score.
highest_average_student = student_averages[0]
for student in student_averages:
    if student[1] > highest_average_student[1]:
        highest_average_student = student

# Print the results
print("Average scores of each student:")
for name, average in student_averages:
    print(f"{name}: {average:.2f}")

print("\nStudents with an average score above 75:")
print(above_75_students)

print(f"\nStudent with the highest average score: " +
      f"{highest_average_student[0]} with an average of " +
      f"{highest_average_student[1]:.2f}")
