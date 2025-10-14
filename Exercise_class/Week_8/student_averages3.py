# The data structure is a list of tuples, where each tuple contains 
# a student’s name, math score, and science score
NUM_STUDENTS = 3

students = []
for num in range(1, NUM_STUDENTS + 1):
    # Alice 85 78
    # Bob 70 82
    # David 65 70
    name, math, sci = input(f'Student #{num} (input name, math and science score): ').split()
    students.append((name, int(math), int(sci)))
print(f'{students = }')

# Calculate the average score of each student.
student_averages = [
    (name, (math + science) / 2)
    for name, math, science in students
]

# Create a list of students who have an average score above 75.
above_75_students = [
    name
    for name, average in student_averages
    if average > 75
]

# Find the student with the highest average score.
highest_average_student = student_averages[0]
for name, average in student_averages[1:]:
    if average > highest_average_student[1]:
        highest_student_name = name

# Print the results
print("Average scores of each student:")
for name, average in student_averages:
    print(f"{name}: {average:.2f}")

print("\nStudents with an average score above 75:")
print(above_75_students)

print(f"\nStudent with the highest average score: " +
      f"{highest_average_student[0]} with an average of " +
      f"{highest_average_student[1]:.2f}")
