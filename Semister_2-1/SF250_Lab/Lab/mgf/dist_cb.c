#include "dist.h"

static double	cb_pmf(double x, void *ctx)
{
	return (exp(logpmf(ctx, (size_t)(x + .5))));
}

static double	cb_m(double t, void *ctx)
{
	return (exp(kclosed(ctx, t)));
}

static double	cb_k(double t, void *ctx)
{
	return (kclosed(ctx, t));
}

void	plots(t_dist *d, double mean, double var)
{
	t_curve	c;
	double	sd;

	sd = sqrt(var);
	c.ctx = d;
	c.title = "pmf P(X=k)";
	c.f = cb_pmf;
	c.lo = fmax(0, mean - 4 * sd);
	c.hi = mean + 4 * sd;
	if (c.hi - c.lo < 1)
		c.hi = c.lo + 1;
	plot(&c);
	c.lo = -2;
	c.hi = 2;
	c.title = "M(t)";
	c.f = cb_m;
	if (!(kclosed(d, 2) < 20))
	{
		c.title = "log M(t)  (M itself overflows / is too steep to draw)";
		c.f = cb_k;
	}
	plot(&c);
}
