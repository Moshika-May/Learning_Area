#include "binomial_poisson.h"

static long	max_count(t_bp *b)
{
	long	mx;
	long	r;

	mx = 0;
	r = -1;
	while (++r <= b->top)
		if (b->h[r] > mx)
			mx = b->h[r];
	return (mx);
}

static void	bar(long v, long mx)
{
	int	k;

	k = 0;
	while (k < (int)(W * (double)v / mx + 0.5))
	{
		putchar('#');
		k++;
	}
	putchar('\n');
}

void	print_table(t_bp *b)
{
	long	r;
	long	mx;
	double	bv;
	double	q;

	mx = max_count(b);
	b->tv = 0;
	printf("%3s %9s %9s %9s\n", "r", "observed", "Binomial", "Poisson");
	r = -1;
	while (++r <= b->top)
	{
		bv = exp(lbin(b->n, r, b->p));
		q = exp(lpoi(b->lam, r));
		b->tv += fabs(bv - q);
		printf("%3ld %9.5f %9.5f %9.5f ", r, (double)b->h[r] / b->samples, bv,
			q);
		bar(b->h[r], mx);
	}
}

void	print_stats(t_bp *b)
{
	double	m;
	double	v;

	m = b->s1 / b->samples;
	v = b->s2 / b->samples - m * m;
	printf("\n          observed   Binomial   Poisson\n");
	printf("mean   %10.4f %10.4f %10.4f\n", m, b->lam, b->lam);
	printf("var    %10.4f %10.4f %10.4f   (Poisson: mean = var)\n", v, b->lam
		* (1 - b->p), b->lam);
	printf("sum |Binomial - Poisson| over shown r = %.5f\n", b->tv);
	printf("Rule of thumb (n > 50, p < 0.1): ");
	if (b->n > 50 && b->p < 0.1)
		printf("satisfied, approximation should be good\n");
	else
		printf("NOT satisfied, expect a visible gap\n");
}
