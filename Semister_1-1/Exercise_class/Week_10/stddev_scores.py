def cal_variance(scores):
    mean = sum(scores) / len(scores)
    sum_diff = 0
    for score in scores:
        diff = score - mean
        sum_diff += diff ** 2
    variance = sum_diff / len(scores)
    return variance

def cal_stddev(scores):
    variance = cal_variance(scores)
    stddev = variance ** 0.5
    return stddev

def main():
    scores = input("Input scores: ").split()
    # scores = [int(score) for score in scores]
    scores = list(map(int, scores))
    stddev = cal_stddev(scores)
    variance = cal_variance(scores)
    print(f'Standard Deviation = {stddev:.2f}')

main()