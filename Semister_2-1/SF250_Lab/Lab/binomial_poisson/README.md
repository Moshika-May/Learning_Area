# Binomial vs Poisson Approximation

When n is large and p is small, the Binomial distribution B(n, p) is very
close to the Poisson distribution Po(np). This program simulates a Binomial
experiment and puts the observed frequencies next to both exact
distributions so you can see how close they are.

## Build and run

```
make
./binomial_poisson [n] [p] [samples] [seed]
```

| Argument | Meaning | Default |
|---|---|---|
| `n` | trials per experiment (>= 1) | 100 |
| `p` | success probability per trial, 0 < p < 1 | 0.05 |
| `samples` | how many experiments to simulate (>= 1) | 100000 |
| `seed` | random seed | current time |

The run costs about `samples * n` random draws, so very large values of both
make it slow.

## How it works

1. **Simulation.** One experiment makes `n` Bernoulli(p) trials and counts the
   successes `x`. This repeats `samples` times, and the frequency of each
   `x` is recorded.
2. **Exact probabilities.** For each r it computes
   - Binomial: `C(n,r) p^r (1-p)^(n-r)`
   - Poisson with `lambda = np`: `lambda^r e^(-lambda) / r!`

   Both are computed in log form with `lgamma`, so large n does not overflow.
3. **Table.** Rows run from r = 0 up to about `lambda + 6*sqrt(lambda) + 5`
   (or n if smaller), where the probabilities are negligible. The `#` bars
   show the observed frequency.
4. **Summary.** It prints the observed mean and variance next to the theory
   (Binomial: `np` and `np(1-p)`, Poisson: both equal `lambda`), the sum of
   `|Binomial - Poisson|` over the shown rows, and whether the rule of thumb
   `n > 50` and `p < 0.1` holds.

## Makefile shortcuts

```
make                          build ./binomial_poisson
make run                      build and run: ./binomial_poisson 100 0.05 100000 1
make run ARGS="10 0.5 50000"  run with your own arguments
make clean                    remove the program
```

## Examples

Good approximation (the defaults):

```
$ ./binomial_poisson 100 0.05 100000 1
== Binomial B(n=100, p=0.05) vs Poisson Po(lambda=np=5), 100000 samples, seed=1 ==
  r  observed  Binomial   Poisson
  3   0.14165   0.13958   0.14037 ###############################
  4   0.18000   0.17814   0.17547 ########################################
  5   0.17958   0.18002   0.17547 ########################################
  ...
          observed   Binomial   Poisson
mean       4.9989     5.0000     5.0000
var        4.7570     4.7500     5.0000   (Poisson: mean = var)
sum |Binomial - Poisson| over shown r = 0.02520
Rule of thumb (n > 50, p < 0.1): satisfied, approximation should be good
```

Poor approximation (compare the sum of differences, about 0.33 here):

```
./binomial_poisson 10 0.5 50000 1
```

What to notice:
- The observed column follows the **Binomial** column. The Poisson column is
  only an approximation of it.
- The variance shows the difference: the Binomial has `np(1-p)` while the
  Poisson insists on `np`. The approximation is good when `1-p` is close to 1.

## Files

- `binomial_poisson.c`: argument parsing and `main`.
- `binomial_poisson_math.c`: the log-probabilities and the simulation.
- `binomial_poisson_print.c`: the table and the summary.
- `binomial_poisson.h`: shared structure and prototypes.
- `Makefile`: `make`, `make run`, `make clean`, `make re`.
