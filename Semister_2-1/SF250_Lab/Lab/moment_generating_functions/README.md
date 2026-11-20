# Moment Generating Functions in C

Two programs that compute an MGF two ways and check they agree:

1. **Closed form**, the textbook formula.
2. **Brute force**, straight from the definition `M(t) = E[e^{tX}]`
   (a sum for discrete, an integral for continuous).

If both columns match, the formula is right. That is the whole experiment.

## Build and run

```
make          # builds both programs
make run      # runs one example of each (make run-discrete / run-continuous for one)
make run-discrete ARGS_D="poisson 4"        # your own arguments
make run-continuous ARGS_C="uniform 0 2"
make test     # one small example per distribution
make big      # stress test: n = 1e9, lambda = 1e11, 2e7 integration steps
make clean
```

## What is an MGF?

`M(t) = E[e^{tX}]`. It packs every moment of X into one function:

- `M(0) = 1` always.
- `M'(0) = E[X]` (the mean).
- `M''(0) = E[X^2]`, so `Var(X) = M''(0) - M'(0)^2`.

Better for computing, take `K(t) = log M(t)` (the cumulant function):

- `K'(0) = mean`
- `K''(0) = variance`

The programs use K because for big n, `M(t)` is astronomically large. With
n = 1e9, `M(1)` is about `e^(3.6e8)`, which overflows a double, but `K(1)` is just 3.6e8.

## Program 1: `discrete_moment_generating_function`

| Distribution | Usage | M(t) | mean | variance |
|---|---|---|---|---|
| Bernoulli(p) | `./discrete_moment_generating_function bernoulli 0.3` | `1-p+p·e^t` | p | p(1-p) |
| Binomial(n,p) | `./discrete_moment_generating_function binomial 20 0.4` | `(1-p+p·e^t)^n` | np | np(1-p) |
| Poisson(λ) | `./discrete_moment_generating_function poisson 4` | `exp(λ(e^t-1))` | λ | λ |

Notes:
- `n` is a `size_t`, so it can be as large as about 1.8e19.
- Bernoulli is just Binomial with n = 1.
- The brute-force sum only visits k within 12 standard deviations of the
  mean, so n = 1e9 takes under a second.
- Expect a small error at huge n (about 5e-7 at n = 1e9). `lgamma` loses
  precision when its argument is that large. It is not a bug.

## Program 2: `continuous_moment_generating_function`

| Distribution | Usage | M(t) | mean | variance |
|---|---|---|---|---|
| Uniform(a,b) | `./continuous_moment_generating_function uniform 0 2` | `(e^{tb}-e^{ta}) / (t(b-a))` | (a+b)/2 | (b-a)²/12 |
| Exponential(λ) | `./continuous_moment_generating_function exponential 2` | `λ/(λ-t)`, only for `t<λ` | 1/λ | 1/λ² |
| Gaussian(μ,σ) | `./continuous_moment_generating_function gaussian 1 2` | `exp(μt + σ²t²/2)` | μ | σ² |

Add a last number to set the Simpson integration steps, e.g.
`./continuous_moment_generating_function gaussian 1 2 100000000`. More steps means a smaller error
but a slower run. The default is 1,000,000.

## Reading the output

```
         t         K closed      K brute-sum       |diff|   (K = log M)
     -1.00       -5.8297387       -5.8297387            0
      ...
moments from derivatives of K at t=0 ...
  mean  numeric 8.0000002  theory 8
  var   numeric 4.7999998  theory 4.8
```

- **K closed** is the formula. **K brute-sum** (or **K integral**) is the
  direct computation. **|diff|** is their gap and should be tiny.
- **mean / var numeric** are `K'(0)` and `K''(0)` estimated with finite
  differences. They should match the theory column to several digits.
- The two ASCII graphs are the pmf/pdf, then `M(t)`. If `M(t)` is too steep
  to draw, the program plots `log M(t)` instead and says so.

## Things to try

1. `./discrete_moment_generating_function binomial 20 0.4`: mean 8, variance 4.8. Check the graphs.
2. `./discrete_moment_generating_function poisson 4` vs `poisson 400`. The pmf turns into a bell
   curve, and `log M` stays a clean curve.
3. `./discrete_moment_generating_function binomial 1000 0.5` next to `./continuous_moment_generating_function gaussian 500 15.8`.
   The binomial is close to a Gaussian, so their `K(t)` agree near t = 0.
4. `./continuous_moment_generating_function exponential 2`. The table's t values stop short of
   λ because M(t) blows up as `t → λ`.
5. `./continuous_moment_generating_function uniform 0 2` vs `uniform -1 1`. Shifting the interval
   multiplies M(t) by `e^{tc}`, which shifts K by `tc`.

## Files

Code follows the 42 Norm (`norminette` passes): no `for`, no ternary, at most
25 lines per function and 5 functions per file, so each program is split up.

- `discrete_moment_generating_function.c`: argument parsing and `main` (Bernoulli, Binomial, Poisson).
- `discrete.h`, `discrete_math.c`, `discrete_num.c`, `discrete_out.c`, `discrete_cb.c`: closed form,
  brute-force sum, printing and plot callbacks for the discrete program.
- `continuous_moment_generating_function.c`: argument parsing and `main` (Uniform, Exponential, Gaussian).
- `continuous.h`, `continuous_math.c`, `continuous_num.c`, `continuous_out.c`, `continuous_cb.c`: same split
  for the continuous program (Simpson integral in `continuous_num.c`).
- `plot.h`, `plot.c`: the ASCII plotter both programs share.
- `Makefile`: build, run, test, big, clean.
