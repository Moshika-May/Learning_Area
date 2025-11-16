# 6810742293 Kasidej Mahanin

def calculate_section_average(section_scores):
    section_averages = []
    no_sections = int(input('Input number of CN101 sections: '))
    for section_score in section_scores:
        section_name = section_score[0]
        scores = section_score[1:]
        average = sum(scores) / len(scores)
        section_averages.append((section_name, average))
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
    return section_name, average

def print_section_scores(section_scores):
    for section_score in section_scores:
        section_name = section_score[0]
        scores = section_score[1:]
        print(f'{section_name}: {scores}')

def print_section_averages(section_averages):
    for section_average in section_averages:
        section_name = section_average[0]
        average = section_average[1]
        print(f'{section_name} average score: {average:.2f}')

def find_max_score(section_scores):
    all_scores = []
    for section_score in section_scores:
        all_scores += section_score[1:]
    max_score = max(all_scores)
    print(f'Maximum score: {max_score}')

def main():
    section_scores = []
    calculate_section_average(section_scores)
    print_section_scores(section_scores)
    print_section_averages(section_scores)
    find_max_score(section_scores)

main()