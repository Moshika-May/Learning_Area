# Waiting Time at a Bus Stop

Buses arrive on average every T minutes. How long does a passenger who shows
up at a random moment wait? This program compares two kinds of bus service
with the same average rate and shows that the average wait is not the same.

1. **Regular buses**: one bus exactly every T minutes. The wait is
   Uniform[0, T], so the mean wait is T/2.
2. **Random buses**: arrivals follow a Poisson process with rate 1/T. The wait
   is Exponential with mean T.

Same rate, but the random service makes you wait twice as long on average.

## Build and run

```
gcc -Wall -Wextra -O2 waiting_times.c -o waiting_times -lm
./waiting_times
```

The program asks two questions:

| Prompt | Meaning |
|---|---|
| `Average bus interval T` | average minutes between buses, for example 15 |
| `Number of samples` | how many simulated passengers, for example 100000 |

The random seed is fixed (250), so the same inputs always give the same output.

## How it works

For each simulated passenger two waiting times are drawn from one uniform
random number `u` in (0, 1):

- regular: `T * u`, which is Uniform[0, T]
- random: `-T * ln(u)`, which is Exponential with mean T (a uniform number
  pushed through `-ln` gives an exponential one)

Each wait is dropped into a histogram bin of width T/10. There are 30 bins
covering 0 to 3T, and the last bin also collects any wait of 3T or more. The
program prints the two histograms with the sample mean next to the theory.

## Example

```
$ printf '15\n100000\n' | ./waiting_times

1) Regular buses: Uniform[0,T]  (mean = 7.517)
  0.00-  1.50 |################################################ 9886
  1.50-  3.00 |################################################# 10036
  ...
   theory T/2 = 7.500

2) Random buses: Exponential(1/T)  (mean = 14.998)
  ...
   theory T = 15.000   (last bar includes waits >= 3T)
```

How to read it:
- The first histogram is flat, so every wait between 0 and T is equally likely.
- The second falls off like `e^(-x/T)`: short waits are common, but a long
  tail of 30, 40 minutes or more pulls the mean up to T.

Try `T = 15` with 100 samples and then 1,000,000 samples: the means move
closer to 7.5 and 15.

## Files

- `waiting_times.c`: the whole program.
