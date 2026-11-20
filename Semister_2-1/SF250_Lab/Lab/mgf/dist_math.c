#include "dist.h"

double	lae(double a, double b)
{
	return (fmax(a, b) + log1p(exp(-fabs(a - b))));
}

double	kclosed(t_dist *d, double t)
{
	if (d->poisson)
		return (d->lam * expm1(t));
	return ((double)d->n * lae(log1p(-d->p), log(d->p) + t));
}

double	logpmf(t_dist *d, size_t k)
{
	double	lg;

	if (d->poisson)
		return (k * log(d->lam) - d->lam - lgamma(k + 1.0));
	lg = lgamma(d->n + 1.0) - lgamma(k + 1.0);
	lg = lg - lgamma((double)(d->n - k) + 1.0);
	return (lg + k * log(d->p) + (double)(d->n - k) * log1p(-d->p));
}
