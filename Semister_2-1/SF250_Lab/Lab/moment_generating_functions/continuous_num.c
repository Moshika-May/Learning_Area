#include "continuous.h"

static int	range(t_cont *c, double t, double *lo, double *hi)
{
	if (c->kind == 'u')
	{
		*lo = c->a;
		*hi = c->b;
	}
	else if (c->kind == 'e')
	{
		if (t >= c->lam)
			return (0);
		*lo = 0;
		*hi = 60 / (c->lam - t);
	}
	else
	{
		*lo = c->mu + c->sg * c->sg * t - 12 * c->sg;
		*hi = c->mu + c->sg * c->sg * t + 12 * c->sg;
	}
	return (1);
}

static double	weight(size_t i, size_t n)
{
	if (i == 0 || i == n)
		return (1);
	if (i % 2)
		return (4);
	return (2);
}

static double	vmax(t_cont *c, double t, double *r)
{
	double	d;
	double	m;
	double	x;
	size_t	i;

	d = (r[1] - r[0]) / c->n;
	m = -INFINITY;
	i = -1;
	while (++i <= c->n)
	{
		x = r[0] + i * d;
		m = fmax(m, logpdf(c, x) + t * x);
	}
	return (m);
}

static double	vsum(t_cont *c, double t, double *r, double m)
{
	double	d;
	double	s;
	double	x;
	size_t	i;

	d = (r[1] - r[0]) / c->n;
	s = 0;
	i = -1;
	while (++i <= c->n)
	{
		x = r[0] + i * d;
		s += weight(i, c->n) * exp(logpdf(c, x) + t * x - m);
	}
	return (s * d / 3);
}

double	knum(t_cont *c, double t)
{
	double	r[2];
	double	m;

	if (!range(c, t, &r[0], &r[1]))
		return (NAN);
	m = vmax(c, t, r);
	return (m + log(vsum(c, t, r, m)));
}
