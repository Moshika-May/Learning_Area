/* MGF of Bernoulli / Binomial / Poisson. Closed form vs brute-force sum of e^{tk}P(k).
 * Everything is in log-space (K(t)=log M(t)), so n up to ~1e18 (size_t) does not overflow.
 * The brute-force sum only visits k within 12 sd of the tilted mean, so cost ~ sqrt(n). */
#include <stdlib.h>
#include "plot.h"

static int poisson;
static size_t n;
static double p, lam;

static double lae(double a, double b) { return fmax(a, b) + log1p(exp(-fabs(a - b))); }

static double Kclosed(double t) { return poisson ? lam * expm1(t) : (double)n * lae(log1p(-p), log(p) + t); }

static double logpmf(size_t k) {
    if (poisson) return k * log(lam) - lam - lgamma(k + 1.0);
    return lgamma(n + 1.0) - lgamma(k + 1.0) - lgamma((double)(n - k) + 1.0) + k * log(p) + (double)(n - k) * log1p(-p);
}

static double Knum(double t) {
    double mu, sd, m = -INFINITY, s = 0;
    if (poisson) { mu = lam * exp(t); sd = sqrt(mu); }
    else { double q = exp(log(p) + t - lae(log1p(-p), log(p) + t)); mu = n * q; sd = sqrt(n * q * (1 - q)); }
    double flo = fmax(0, mu - 12 * sd - 5), fhi = mu + 12 * sd + 5;
    size_t lo = (size_t)flo, hi = poisson ? (size_t)fhi : (fhi > (double)n ? n : (size_t)fhi);
    for (size_t k = lo; k <= hi; k++) m = fmax(m, logpmf(k) + t * k);
    for (size_t k = lo; k <= hi; k++) s += exp(logpmf(k) + t * k - m);
    return m + log(s);
}

static double pmf(double x) { return exp(logpmf((size_t)(x + .5))); }
static double plotM(double t) { return exp(Kclosed(t)); }

int main(int argc, char **argv) {
    const char *name = argc > 1 ? argv[1] : "";
    if (!strcmp(name, "bernoulli") && argc == 3) { n = 1; p = atof(argv[2]); }
    else if (!strcmp(name, "binomial") && argc == 4) { n = strtoull(argv[2], 0, 10); p = atof(argv[3]); }
    else if (!strcmp(name, "poisson") && argc == 3) { poisson = 1; lam = atof(argv[2]); }
    else {
        fprintf(stderr, "usage: %s bernoulli p | binomial n p | poisson lambda\n"
                        "e.g.   %s binomial 1000000000 0.3\n", argv[0], argv[0]);
        return 1;
    }
    if (!poisson && !(p > 0 && p < 1)) { fprintf(stderr, "need 0<p<1\n"); return 1; }
    if (poisson && !(lam > 0)) { fprintf(stderr, "need lambda>0\n"); return 1; }

    double mean = poisson ? lam : n * p, var = poisson ? lam : n * p * (1 - p);
    if (poisson) printf("Poisson(lambda=%g)\n", lam);
    else printf("%s(n=%zu, p=%g)\n", n == 1 ? "Bernoulli" : "Binomial", n, p);
    printf("M(t) = E[e^{tX}] = %s\n", poisson ? "exp(lambda (e^t - 1))" : "(1-p+p e^t)^n");
    printf("\n%8s %16s %16s %12s   (K = log M)\n", "t", "K closed", "K brute-sum", "|diff|");
    double ts[] = {-1, -.5, -.1, 0, .1, .5, .9};
    for (int i = 0; i < 7; i++) {
        double a = Kclosed(ts[i]), b = Knum(ts[i]);
        printf("%8.2f %16.8g %16.8g %12.3g\n", ts[i], a, b, fabs(a - b));
    }
    double h = 1e-3, k1 = Kclosed(h), k0 = Kclosed(-h);
    printf("\nmoments from derivatives of K at t=0 (K'(0)=mean, K''(0)=var):\n"
           "  mean  numeric %.8g  theory %.8g\n  var   numeric %.8g  theory %.8g\n",
           (k1 - k0) / (2 * h), mean, (k1 - 2 * Kclosed(0) + k0) / (h * h), var);

    double sd = sqrt(var), plo = fmax(0, mean - 4 * sd), phi = mean + 4 * sd;
    if (phi - plo < 1) phi = plo + 1;
    plot("pmf P(X=k)", pmf, plo, phi);
    if (Kclosed(2) < 20) plot("M(t)", plotM, -2, 2);
    else plot("log M(t)  (M itself overflows / is too steep to draw)", Kclosed, -2, 2);
    return 0;
}
