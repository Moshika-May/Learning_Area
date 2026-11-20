# Central Limit Theorem Demo

The Central Limit Theorem says that the average of many independent draws
looks Normal, even when each draw is not Normal. This program draws samples
from a skewed or flat population, computes many sample means, and compares
their distribution with the standard Normal curve.

## Build and run

```
make
./clt [uniform|exp] [n] [reps] [seed]
```

| Argument | Meaning | Default |
|---|---|---|
| `uniform` or `exp` | population: Uniform(0,1) or Exponential(1) | `uniform` |
| `n` | sample size (draws per mean, >= 1) | 30 |
| `reps` | how many sample means to compute (>= 1) | 10000 |
| `seed` | random seed | current time |

## How it works

1. **Population.** Uniform(0,1) has mean 1/2 and variance 1/12. Exponential(1)
   has mean 1 and variance 1, and is strongly skewed to the right. Exponential
   values are made from uniform ones with `-ln(u)`.
2. **Sampling.** For each of `reps` repetitions it averages `n` draws to get
   a sample mean `xbar`.
3. **Standardising.** Each mean becomes `z = (xbar - mu) / (sigma / sqrt(n))`.
   By the CLT, z is close to N(0, 1) when n is large.
4. **Histogram.** The z values fall into 16 bins of width 0.5 covering
   [-4, 4). Next to each bin it prints the count expected from N(0, 1),
   computed with the Normal CDF. Values outside [-4, 4) are not shown.
5. **Summary.** The mean of z should be about 0, the variance about 1, and
   the skewness about `population skewness / sqrt(n)` (2 for Exponential,
   0 for Uniform). The skewness shrinks as n grows, which is the CLT at work.

## Examples

```
$ ./clt exp 30 10000 1
== CLT: population=Exp(1), sample size n=30, repetitions=10000, seed=1 ==
Histogram of z = (xbar - mu)/(sigma/sqrt n): observed (#) vs Normal(0,1) expected
    z range     obs  expected
[-2.5,-2.0)     109     165.4 ##
[-2.0,-1.5)     455     440.6 #########
 ...
mean(z)=-0.0123 (theory 0)  var(z)=0.9935 (theory 1)  skewness=+0.3535 (theory +0.3651 = pop. skew/sqrt n -> 0)
```

Things to try:
- `./clt exp 1`, `exp 5`, `exp 30`, `exp 200`: at n = 1 the histogram is the
  lopsided Exponential, and by n = 200 it is nearly symmetric.
- `./clt uniform 1` versus `./clt uniform 30`: even a flat population turns
  bell-shaped once you average.
- Raise `reps` (for example 200000) to make the observed counts hug the
  expected ones more closely.

## Files

- `clt.c`: argument parsing and `main`.
- `clt_sim.c`: the sampling and the Normal CDF.
- `clt_print.c`: the histogram and the summary.
- `clt.h`: shared structure and prototypes.
- `Makefile`: `make`, `make clean`.
