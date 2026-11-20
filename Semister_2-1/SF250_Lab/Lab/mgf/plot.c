#include "plot.h"

static void	sample(t_plot *p, t_curve *c)
{
	int	i;

	p->ymin = INFINITY;
	p->ymax = -INFINITY;
	i = -1;
	while (++i < PW)
	{
		p->y[i] = c->f(c->lo + (c->hi - c->lo) * i / (PW - 1), c->ctx);
		if (isfinite(p->y[i]))
		{
			p->ymin = fmin(p->ymin, p->y[i]);
			p->ymax = fmax(p->ymax, p->y[i]);
		}
	}
	if (!(p->ymax > p->ymin))
		p->ymax = p->ymin + 1;
}

static int	row_of(t_plot *p, int i)
{
	return ((int)((p->ymax - p->y[i]) / (p->ymax - p->ymin) * (PH - 1) + .5));
}

static void	fill(t_plot *p)
{
	int	r;
	int	i;

	memset(p->g, ' ', sizeof(p->g));
	r = -1;
	while (++r < PH)
		p->g[r][PW] = 0;
	i = -1;
	while (++i < PW)
		if (isfinite(p->y[i]))
			p->g[row_of(p, i)][i] = '*';
}

static void	show(t_plot *p, t_curve *c)
{
	int	r;

	printf("\n%s\n", c->title);
	r = -1;
	while (++r < PH)
		printf("%11.4g |%s\n", p->ymax - (p->ymax - p->ymin) * r / (PH - 1),
			p->g[r]);
	printf("%11s +", "");
	r = -1;
	while (++r < PW)
		putchar('-');
	printf("\n%11s  %-*.4g%.4g\n", "", PW - 8, c->lo, c->hi);
}

void	plot(t_curve *c)
{
	t_plot	p;

	sample(&p, c);
	fill(&p);
	show(&p, c);
}
