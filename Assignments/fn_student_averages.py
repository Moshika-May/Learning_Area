# 6810742293 Kasidej Mahanin

# Define function
def calculate_averages(students):
    averages = []

    for name, math_score, science_score in students:
        average = (math_score + science_score) / 2
        averages.append((name, average))

    return averages

def get_students_above_threshold(averages, threshold=75):
    above_threshold = []

    for name, average in averages:
        if average > threshold:
            above_threshold.append(name)

    return above_threshold

def get_highest_average_student(averages):
    highest_student_name = None
    highest_score = -1

    if not averages:
        return (None, -1)

    for name, average in averages:
        if average > highest_score:
            highest_score = average
            highest_student_name = name
            
    return (highest_student_name, highest_score)

def print_report(averages, above_threshold, highest):
    highest_name, highest_score = highest
    
    print("Student averages:")
    for name, average in averages:
        print(f"{name}: {average:.2f}")
        
    print("\nStudents with an average score above 75:")
    print(above_threshold)
    
    if highest_name is not None:
        print(f"\nStudent with the highest average score: "
              f"{highest_name} with an average of {highest_score:.2f}")
    else:
        print("\nNo student data to report.")

def main():
    students = [
        ("Alice", 85, 90),
        ("Bob", 78, 82),
        ("Charlie", 92, 93),
        ("David", 65, 70),
        ("Eve", 88, 85)
    ]
    
    averages = calculate_averages(students)
    above_threshold = get_students_above_threshold(averages, 75)
    highest = get_highest_average_student(averages)
    
    print_report(averages, above_threshold, highest)

main()