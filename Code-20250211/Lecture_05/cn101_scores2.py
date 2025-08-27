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

# Calculates and returns the average score for each section.
section_averages = [
    (section_score[0], sum(section_score[1:]) / len(section_score[1:]))
    for section_score in section_scores
]

# Prints the scores for each section.
for section_score in section_scores:
    section_name = section_score[0]
    scores = section_score[1:]
    print(f'{section_name}: {scores}')

# Prints the average score for each section.
for section_name, average in section_averages:
    print(f'{section_name} average score: {average:.2f}')

# Finds and returns the maximum score across all sections.
max_score = max([
    score
    for section_score in section_scores
    for score in section_score[1:]
])

print(f'Maximum score: {max_score}')
