# Coin Flip Simulation

Flip a (possibly biased) coin N times in C, then show how the results behave:
the running proportion of heads settles toward the true probability, the
number of heads per group follows a Binomial distribution, and a simple
z-test decides whether the coin looks fair.

## Build and run

```
make
./coin [N] [p_head] [seed]
```

| Argument | Meaning | Default |
|---|---|---|
| `N` | number of flips (must be >= 10) | 1000 |
| `p_head` | probability of heads, 0 < p < 1 | 0.5 |
| `seed` | random seed (same seed gives the same run) | current time |

## How it works

1. **Simulation.** Each flip draws a uniform random number and counts a head
   when it is below `p`. Each flip is a Bernoulli(p) trial.
2. **Convergence plot.** At 20 checkpoints, spaced on a log scale, it prints
   the running proportion `p_hat = heads / n`. On the plot `*` is `p_hat` and
   `|` is the true `p`. For small N some checkpoints repeat the same `n`.
3. **Binomial histogram.** The flips are cut into groups of 10. For each
   group it counts the heads (0 to 10), then compares the observed number of
   groups with the Binomial(10, p) expectation `groups * C(10,k) p^k (1-p)^(10-k)`.
4. **Test.** Under H0 (the coin really has probability `p`) the number of
   heads has mean `np` and standard deviation `sqrt(np(1-p))`. It prints
   `z = (heads - np) / SD` and rejects H0 when `|z| >= 1.96` (alpha = 0.05).

## Examples

```
./coin                   # 1000 flips, fair coin
./coin 100000 0.5 42     # 100,000 flips, reproducible
./coin 5000 0.7 1       # biased coin with P(H) = 0.7
```

Output of `./coin 1000 0.5 7` (trimmed):

```
== Coin flip simulation: N=1000, P(H)=0.500, seed=7 ==

Convergence of running proportion (Law of Large Numbers)
        n   p_hat  0                                                 1
     ...
     1000  0.4840                          *|

Heads per group of 10 flips: observed (#) vs binomial expected
  k     obs  expected
  4      25      20.5 #####################################
  5      27      24.6 ########################################
  6      16      20.5 ########################

Heads=484  Tails=516  p_hat=0.4840
Expected heads=500.0  SD=15.81  z=-1.012
H0: P(H)=0.500 at alpha=0.05 -> fail to reject
```

Things to try:
- Raise N (10, 1000, 100000) and watch `*` move onto `|`.
- Run the same N with different seeds; the histogram bars wobble around the
  expected counts.
- The test checks the data against the `p_head` you passed, so it rejects
  only about 5% of runs (that is what alpha = 0.05 means).
- "Fail to reject" does not prove the coin is fair, it only means the data
  are not unusual enough under H0.

## Files

- `coin.c`: argument parsing and `main`.
- `coin_sim.c`: the simulation and the convergence rows.
- `coin_print.c`: the histogram and the summary statistics.
- `coin.h`: shared structure and prototypes.
- `Makefile`: `make`, `make clean`.
