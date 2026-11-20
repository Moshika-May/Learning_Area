#include "coin.h"

static void	row(t_coin *c, long i)
{
	double	ph;
	int		col;
	int		mid;
	int		x;

	ph = (double)c->heads / i;
	col = (int)(ph * (W - 1) + 0.5);
	mid = (int)(c->p * (W - 1) + 0.5);
	printf("%9ld %7.4f  ", i, ph);
	x = -1;
	while (++x < W)
	{
		if (x == col)
			putchar('*');
		else if (x == mid)
			putchar('|');
		else
			putchar(' ');
	}
	putchar('\n');
}

static int	due(t_coin *c, long i, int ci)
{
	return (ci <= NC && i >= (long)ceil(pow((double)c->n, (double)ci / NC)));
}

static void	tally(t_coin *c, long i, int *gh)
{
	if (rand() / (RAND_MAX + 1.0) < c->p)
	{
		c->heads++;
		(*gh)++;
	}
	if (i % K == 0)
	{
		c->hist[*gh]++;
		c->groups++;
		*gh = 0;
	}
}

void	simulate(t_coin *c)
{
	long	i;
	int		gh;
	int		ci;

	gh = 0;
	ci = 1;
	i = 0;
	while (++i <= c->n)
	{
		tally(c, i, &gh);
		while (due(c, i, ci))
		{
			row(c, i);
			ci++;
		}
	}
}
