from math import sqrt

def calc_perfect_numbers(max_exclusive):

    perfect_numbers = []
    for laps in range(1, max_exclusive + 1):
        # print(f'================================ Firstloop = {laps}')
        factor = []

        for times in range(int(sqrt(laps))):
            # print(f'Secondloop = {times}')
            if laps % (times + 1) == 0 and laps != (times + 1):
                factor += [times + 1]
                # print(f'Factor 1 = {factor}')

                if laps / (times + 1) != laps and laps / (times + 1) not in factor:
                    factor += [laps / (times + 1)]
                # print(f'Factor 2 = {factor}')


        if sum(factor) == laps:
            perfect_numbers.append(laps)
            # print(f'Perfect number: {perfect_numbers}')

    # print(f'{perfect_numbers}')
    return perfect_numbers

def main():
    max_exclusive = 30
    calc_perfect_numbers(max_exclusive)

if __name__ == "__main__":
    main()