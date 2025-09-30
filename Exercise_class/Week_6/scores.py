NUM_SCORES = 5

scores = []
for i in range(NUM_SCORES):
    score = int(input('Input a score: '))
    scores += [score]
#     scores.append(score)

print(f'{scores = }')