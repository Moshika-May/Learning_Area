/* MGF of Uniform / Exponential / Gaussian. Closed form vs Simpson integral of e^{tx} f(x).
 * N (size_t, even) = number of Simpson intervals; raise it for more accuracy. Log-space again. */
#include <stdlib.h>
#include "plot.h"

static char kind; /* 'u' 'e' 'g' */
static double a, b, lam, mu, sg;
static size_t N = 1000000;

static double lem(double x) { return x > 0 ? (x > 30 ? x + log1p(-exp(-x)) : log(expm1(x))) - log(x) : log(-expm1(x)) - log(-x); }

static double Kclosed(double t) {
    if (kind == 'u') return fabs(t * (b - a)) < 1e-12 ? t * (a + b) / 2 : t * a + lem(t * (b - a));
    if (kind == 'e') return t < lam ? log(lam) - log(lam - t) : NAN;
    return mu * t + sg * sg * t * t / 2;
}

static double logpdf(double x) {
    if (kind == 'u') return x < a || x > b ? -INFINITY : -log(b - a);
    if (kind == 'e') return x < 0 ? -INFINITY : log(lam) - lam * x;
    return -.5 * (x - mu) * (x - mu) / (sg * sg) - log(sg * sqrt(2 * M_PI));
}

static double Knum(double t) {
    double lo, hi;
    if (kind == 'u') { lo = a; hi = b; }
    else if (kind == 'e') { if (t >= lam) return NAN; lo = 0; hi = 60 / (lam - t); }
    else { lo = mu + sg * sg * t - 12 * sg; hi = mu + sg * sg * t + 12 * sg; }
    double d = (hi - lo) / N, m = -INFINITY, s = 0;
    for (size_t i = 0; i <= N; i++) m = fmax(m, logpdf(lo + i * d) + t * (lo + i * d));
    for (size_t i = 0; i <= N; i++) {
        double x = lo + i * d, w = i == 0 || i == N ? 1 : i % 2 ? 4 : 2;
        s += w * exp(logpdf(x) + t * x - m);
    }
    return m + log(s * d / 3);
}

static double pdf(double x) { return exp(logpdf(x)); }
static double plotM(double t) { return exp(Kclosed(t)); }

int main(int argc, char **argv) {
    const char *name = argc > 1 ? argv[1] : "";
    int na = 0;
    if (!strcmp(name, "uniform") && argc >= 4) { kind = 'u'; a = atof(argv[2]); b = atof(argv[3]); na = 4; }
    else if (!strcmp(name, "exponential") && argc >= 3) { kind = 'e'; lam = atof(argv[2]); na = 3; }
    else if (!strcmp(name, "gaussian") && argc >= 4) { kind = 'g'; mu = atof(argv[2]); sg = atof(argv[3]); na = 4; }
    else {
        fprintf(stderr, "usage: %s uniform a b [N] | exponential lambda [N] | gaussian mu sigma [N]\n"
                        "e.g.   %s gaussian 1 2 100000000\n", argv[0], argv[0]);
        return 1;
    }
    if (argc > na) N = strtoull(argv[na], 0, 10);
    N += N & 1; if (!N) N = 2;
    if ((kind == 'u' && !(b > a)) || (kind == 'e' && !(lam > 0)) || (kind == 'g' && !(sg > 0))) {
        fprintf(stderr, "bad parameters\n"); return 1;
    }

    double mean, var, unit;
    if (kind == 'u') { mean = (a + b) / 2; var = (b - a) * (b - a) / 12; unit = 1 / fmax(fabs(a) + fabs(b), 1e-9); printf("Uniform(a=%g, b=%g)\nM(t) = (e^{tb} - e^{ta}) / (t (b-a))\n", a, b); }
    else if (kind == 'e') { mean = 1 / lam; var = 1 / (lam * lam); unit = lam; printf("Exponential(lambda=%g)\nM(t) = lambda / (lambda - t),  t < lambda\n", lam); }
    else { mean = mu; var = sg * sg; unit = 1 / fmax(fabs(mu) + sg, 1e-9); printf("Gaussian(mu=%g, sigma=%g)\nM(t) = exp(mu t + sigma^2 t^2 / 2)\n", mu, sg); }
    printf("Simpson intervals N=%zu\n\n%10s %16s %16s %12s   (K = log M)\n", N, "t", "K closed", "K integral", "|diff|");
    double ts[] = {-1, -.5, -.1, 0, .1, .5, .9};
    for (int i = 0; i < 7; i++) {
        double t = ts[i] * unit, x = Kclosed(t), y = Knum(t);
        printf("%10.4g %16.8g %16.8g %12.3g\n", t, x, y, fabs(x - y));
    }
    double h = 1e-3 * unit, k1 = Kclosed(h), k0 = Kclosed(-h);
    printf("\nmoments from derivatives of K at t=0:\n  mean  numeric %.8g  theory %.8g\n  var   numeric %.8g  theory %.8g\n",
           (k1 - k0) / (2 * h), mean, (k1 - 2 * Kclosed(0) + k0) / (h * h), var);

    double sd = sqrt(var);
    if (kind == 'u') plot("pdf f(x)", pdf, a - .1 * (b - a), b + .1 * (b - a));
    else if (kind == 'e') plot("pdf f(x)", pdf, 0, mean + 5 * sd);
    else plot("pdf f(x)", pdf, mean - 4 * sd, mean + 4 * sd);
    double tlo = -2 * unit, thi = (kind == 'e' ? .95 : 2) * unit;
    if (Kclosed(thi) < 20) plot("M(t)", plotM, tlo, thi);
    else plot("log M(t)", Kclosed, tlo, thi);
    return 0;
}
