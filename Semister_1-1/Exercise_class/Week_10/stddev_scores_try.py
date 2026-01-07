def get_scores():

    scores_string = input('Input your scores: ').split()
    scores = [int(score_string) for score_string in scores_string]
    return scores

def cal_stddev(scores):

    sum_of_scores = sum(scores)
    n_of_scores = len(scores)
    scores_1 = scores.copy()
    x_bar = sum_of_scores / n_of_scores
    for i in scores:
        scores_1[i] -= x_bar


def main():
    scores = get_scores()
    cal_stddev(scores)

main()