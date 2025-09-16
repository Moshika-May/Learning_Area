total = 0
count = 0
while True:
    score = int(input('Enter a number [1-10](-1 to end): '))
    if score == -1:
        break
    if score < 1 or score > 10:
        print('Error: Incorrect score, please enter a score between 1 and 10.')
        continue

    total += score
    count += 1

if count > 0:
    average = total / count
    print(f'Average score: {average:.2f}')
    print(f'Total score: {total}')