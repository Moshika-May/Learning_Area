# 6810742293 Kasidej Mahanin

# Define function
def calculate_section_average(section_scores):
    averages = []

    for section_name, scores in section_scores:
        if scores:
            average = sum(scores) / len(scores)
        else:
            average = 0.0
        averages.append((section_name, average))
    return averages

def print_section_scores(section_scores):
    print("\nSection Scores:")
    for section_name, scores in section_scores:
        print(f"{section_name}: {scores}")

def print_section_averages(section_averages):
    print("\nSection Averages:")
    for section_name, average in section_averages:
        print(f"{section_name}: {average:.2f}")

def find_max_score(section_scores):
    all_scores = []

    for _, scores in section_scores:
        all_scores.extend(scores)
    
    if not all_scores:
        return 0.0
        
    return max(all_scores)

def main():
    while True:
        no_sections_input = input('Enter the number of sections: ')

        if no_sections_input.isdigit() and int(no_sections_input) > 0:
            no_sections = int(no_sections_input)
            break
        else:
            print("Error: Please enter a valid positive number.")

    section_scores = []
    
    for _ in range(no_sections):
        section_name = input('Enter section name: ')
        scores = []
        
        while True:
            score_input = input(f'Enter score for {section_name} (or -1 to finish): ')
            
            if score_input == "-1":
                break
                
            s_check = score_input
            is_valid = False
            
            if s_check.startswith('-'):
                s_check = s_check[1:]
                
            if s_check:
                if s_check.count('.') <= 1 and s_check.replace('.', '', 1).isdigit():
                    is_valid = True

            if is_valid:
                scores.append(float(score_input))
            else:
                print("Invalid input. Please enter a number or -1.")

        section_scores.append((section_name, scores))
        print()

    print_section_scores(section_scores)
    
    section_averages = calculate_section_average(section_scores)
    print_section_averages(section_averages)
    
    max_score = find_max_score(section_scores)
    print(f"\nMaximum score across all sections: {max_score:.2f}")

# Call function main
main()