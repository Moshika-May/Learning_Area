# 6810742293 Kasidej Mahanin

# Named Constants
QUIZ_WEIGHT = 0.2
MIDTERM_WEIGHT = 0.3
FINAL_WEIGHT = 0.5

# Define Function
def calculate_final_scores(students):
    final_scores = []

    for name, quizzes, midterm, final in students:
        quiz_avg = sum(quizzes) / len(quizzes)
        
        final_score = (quiz_avg * QUIZ_WEIGHT + midterm * MIDTERM_WEIGHT + final * FINAL_WEIGHT)
        
        final_scores.append((name, final_score))

    return final_scores

def assign_letter_grades(final_scores):
    graded = []

    for name, score in final_scores:
        if score >= 80:
            grade = 'A'
        elif score >= 70:
            grade = 'B'
        elif score >= 60:
            grade = 'C'
        elif score >= 50:
            grade = 'D'
        else:
            grade = 'F'
        graded.append((name, score, grade))

    return graded


def get_honors_students(graded_students, threshold=80):
    honors = []

    for name, score, grade in graded_students:
        if score >= threshold:
            honors.append(name)

    return honors

def get_at_risk_students(graded_students, threshold=50):
    at_risk = []

    for name, score, grade in graded_students:
        if score < threshold:
            at_risk.append(name)
    return at_risk

def calculate_overall_statistics(graded_students):
    scores = [score for name, score, grade in graded_students]
    
    if not scores:
        return (0, 0, 0)
        
    class_average = sum(scores) / len(scores)
    highest_score = max(scores)
    lowest_score = min(scores)
    
    return (class_average, highest_score, lowest_score)

def print_report(graded_students, honors_students, at_risk_students, stats):
    class_average, highest_score, lowest_score = stats
    
    print("\nFinal scores and grades of each student:")
    for name, score, grade in graded_students:
        print(f"{name}: {score:.2f} ({grade})")

    print(f"\nHonors students (>= 80):")
    print(honors_students)
    
    print(f"\nAt-risk students (< 50):")
    print(at_risk_students)
    
    print("\nClass statistics:")
    print(f"Average score: {class_average:.2f}")
    print(f"Highest score: {highest_score:.2f}")
    print(f"Lowest score: {lowest_score:.2f}")

def main():
    students = []
    
    while True:
        n_input = input("Enter number of students: ")
        if n_input.isdigit() and int(n_input) > 0:
            n = int(n_input)
            break
        else:
            print("Invalid input. Please enter a positive integer.")

    for i in range(1, n + 1):
        name = input(f"Enter name of student #{i}: ")
        
        while True:
            quiz_str = input(f"Enter 3 quiz scores for {name} (separated by spaces): ")
            parts = quiz_str.split()
            
            if len(parts) != 3:
                print(f"Invalid input. Please enter exactly 3 scores separated by spaces.")
                continue
                
            quizzes = []
            all_valid = True
            
            for part in parts:      # Validation
                s = part
                is_valid = False

                if s:
                    s_check = s
                    if s.startswith('-'):
                        s_check = s[1:]
                    if s_check:
                        if s_check.count('.') <= 1 and s_check.replace('.', '', 1).isdigit():
                            is_valid = True
                
                if is_valid:
                    quizzes.append(float(part))
                else:
                    all_valid = False
                    break
            
            if all_valid:
                break
            else:
                print("Invalid input. One or more scores were not valid numbers. Please try again.")

        while True:
            midterm_input = input(f"Enter midterm score for {name}: ")
            
            s = midterm_input
            is_valid = False
            if s:
                s_check = s
                if s.startswith('-'):
                    s_check = s[1:]
                if s_check:
                    if s_check.count('.') <= 1 and s_check.replace('.', '', 1).isdigit():
                        is_valid = True
            
            if is_valid:
                midterm = float(midterm_input)
                break
            else:
                print("Invalid input. Please enter a valid number.")

        while True:
            final_input = input(f"Enter final exam score for {name}: ")
            
            s = final_input
            is_valid = False
            if s:
                s_check = s
                if s.startswith('-'):
                    s_check = s[1:]
                if s_check:
                    if s_check.count('.') <= 1 and s_check.replace('.', '', 1).isdigit():
                        is_valid = True
            
            if is_valid:
                final = float(final_input)
                break
            else:
                print("Invalid input. Please enter a valid number.")
        
        students.append((name, quizzes, midterm, final))
        print()

    final_scores = calculate_final_scores(students)
    graded_students = assign_letter_grades(final_scores)
    
    honors_students = get_honors_students(graded_students) 
    at_risk_students = get_at_risk_students(graded_students)
    
    stats = calculate_overall_statistics(graded_students)
    
    print_report(graded_students, honors_students, at_risk_students, stats)

main()