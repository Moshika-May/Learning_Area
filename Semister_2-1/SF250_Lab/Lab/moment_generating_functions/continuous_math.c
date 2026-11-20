#include "continuous.h"

static double	lem(double x)
{
	if (x > 0)
	{
		if (x > 30)
			return (x + log1p(-exp(-x)) - log(x));
		return (log(expm1(x)) - log(x));
	}
	return (log(-expm1(x)) - log(-x));
}

double	kclosed(t_cont *c, double t)
{
	if (c->kind == 'u')
	{
		if (fabs(t * (c->b - c->a)) < 1e-12)
			return (t * (c->a + c->b) / 2);
		return (t * c->a + lem(t * (c->b - c->a)));
	}
	if (c->kind == 'e')
	{
		if (t < c->lam)
			return (log(c->lam) - log(c->lam - t));
		return (NAN);
	}
	return (c->mu * t + c->sg * c->sg * t * t / 2);
}

double	logpdf(t_cont *c, double x)
{
	double	z;

	if (c->kind == 'u')
	{
		if (x < c->a || x > c->b)
			return (-INFINITY);
		return (-log(c->b - c->a));
	}
	if (c->kind == 'e')
	{
		if (x < 0)
			return (-INFINITY);
		return (log(c->lam) - c->lam * x);
	}
	z = x - c->mu;
	return (-.5 * z * z / (c->sg * c->sg) - log(c->sg * sqrt(2 * M_PI)));
}

void	setup(t_cont *c)
{
	if (c->kind == 'u')
	{
		c->mean = (c->a + c->b) / 2;
		c->var = (c->b - c->a) * (c->b - c->a) / 12;
		c->unit = 1 / fmax(fabs(c->a) + fabs(c->b), 1e-9);
	}
	else if (c->kind == 'e')
	{
		c->mean = 1 / c->lam;
		c->var = 1 / (c->lam * c->lam);
		c->unit = c->lam;
	}
	else
	{
		c->mean = c->mu;
		c->var = c->sg * c->sg;
		c->unit = 1 / fmax(fabs(c->mu) + c->sg, 1e-9);
	}
}

int	check_params(t_cont *c)
{
	int	bad;

	bad = 0;
	if (c->kind == 'u' && !(c->b > c->a))
		bad = 1;
	if (c->kind == 'e' && !(c->lam > 0))
		bad = 1;
	if (c->kind == 'g' && !(c->sg > 0))
		bad = 1;
	if (bad)
		fprintf(stderr, "bad parameters\n");
	return (bad);
}
