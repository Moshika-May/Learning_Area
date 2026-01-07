no_sections = int(input('Input number of CN101 sections: '))

# Input scores for each section.
section_scores = []
for _ in range(no_sections):
    section_name = input('Input CN101 section name: ')
    scores = []
    print(f'Input scores for {section_name} section (type -1 to stop):')
    count = 1
    while True:
        score = float(input(f'Input score #{count}: '))
        if score == -1:
            break
        scores.append(score)
        count += 1
    scores.insert(0, section_name)
    section_scores.append(scores)

# Calculates the average score for each section.
section_averages = []
for section_score in section_scores:
    section_name = section_score[0]
    scores = section_score[1:]
    average = sum(scores) / len(scores)
    section_averages.append((section_name, average))

# Prints the scores for each section.
for section_score in section_scores:
    section_name = section_score[0]
    scores = section_score[1:]
    print(f'{section_name}: {scores}')

# Prints the average score for each section.
for section_average in section_averages:
    section_name = section_average[0]
    average = section_average[1]
    print(f'{section_name} average score: {average:.2f}')

# Finds the maximum score across all sections.
all_scores = []
for section_score in section_scores:
    all_scores += section_score[1:]
max_score = max(all_scores)
print(f'Maximum score: {max_score}')
