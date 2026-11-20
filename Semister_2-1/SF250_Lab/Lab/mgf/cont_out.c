#include "cont.h"

static const double	g_ts[7] = {-1, -.5, -.1, 0, .1, .5, .9};

void	print_title(t_cont *c)
{
	if (c->kind == 'u')
	{
		printf("Uniform(a=%g, b=%g)\n", c->a, c->b);
		printf("M(t) = (e^{tb} - e^{ta}) / (t (b-a))\n");
	}
	else if (c->kind == 'e')
	{
		printf("Exponential(lambda=%g)\n", c->lam);
		printf("M(t) = lambda / (lambda - t),  t < lambda\n");
	}
	else
	{
		printf("Gaussian(mu=%g, sigma=%g)\n", c->mu, c->sg);
		printf("M(t) = exp(mu t + sigma^2 t^2 / 2)\n");
	}
}

void	print_intro(t_cont *c)
{
	printf("Simpson intervals N=%zu\n\n", c->n);
	printf("%10s %16s %16s %12s   (K = log M)\n", "t", "K closed", "K integral",
		"|diff|");
}

void	print_table(t_cont *c)
{
	int		i;
	double	t;
	double	x;
	double	y;

	i = -1;
	while (++i < 7)
	{
		t = g_ts[i] * c->unit;
		x = kclosed(c, t);
		y = knum(c, t);
		printf("%10.4g %16.8g %16.8g %12.3g\n", t, x, y, fabs(x - y));
	}
}

void	print_moments(t_cont *c)
{
	double	h;
	double	k1;
	double	k0;

	h = 1e-3 * c->unit;
	k1 = kclosed(c, h);
	k0 = kclosed(c, -h);
	printf("\nmoments from derivatives of K at t=0:\n");
	printf("  mean  numeric %.8g  theory %.8g\n", (k1 - k0) / (2 * h), c->mean);
	printf("  var   numeric %.8g  theory %.8g\n", (k1 - 2 * kclosed(c, 0) + k0)
		/ (h * h), c->var);
}
