#include "continuous.h"

static double	cb_pdf(double x, void *ctx)
{
	return (exp(logpdf(ctx, x)));
}

static double	cb_m(double t, void *ctx)
{
	return (exp(kclosed(ctx, t)));
}

static double	cb_k(double t, void *ctx)
{
	return (kclosed(ctx, t));
}

static void	pdf_range(t_cont *c, t_curve *cv)
{
	double	sd;

	sd = sqrt(c->var);
	if (c->kind == 'u')
	{
		cv->lo = c->a - .1 * (c->b - c->a);
		cv->hi = c->b + .1 * (c->b - c->a);
	}
	else if (c->kind == 'e')
	{
		cv->lo = 0;
		cv->hi = c->mean + 5 * sd;
	}
	else
	{
		cv->lo = c->mean - 4 * sd;
		cv->hi = c->mean + 4 * sd;
	}
}

void	plots(t_cont *c)
{
	t_curve	cv;

	cv.ctx = c;
	cv.title = "pdf f(x)";
	cv.f = cb_pdf;
	pdf_range(c, &cv);
	plot(&cv);
	cv.lo = -2 * c->unit;
	cv.hi = 2 * c->unit;
	if (c->kind == 'e')
		cv.hi = .95 * c->unit;
	cv.title = "M(t)";
	cv.f = cb_m;
	if (!(kclosed(c, cv.hi) < 20))
	{
		cv.title = "log M(t)";
		cv.f = cb_k;
	}
	plot(&cv);
}
