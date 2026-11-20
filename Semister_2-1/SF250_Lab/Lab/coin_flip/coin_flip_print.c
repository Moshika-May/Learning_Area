#include "coin_flip.h"

static void	bar(int n)
{
	while (n-- > 0)
		putchar('#');
	putchar('\n');
}

static double	expected(t_coin *c, int k)
{
	return (c->groups * tgamma(K + 1) / (tgamma(k + 1) * tgamma(K - k + 1))
		* pow(c->p, k) * pow(1 - c->p, K - k));
}

void	print_hist(t_coin *c)
{
	int		k;
	double	maxc;

	printf("\nHeads per group of %d flips: ", K);
	printf("observed (#) vs binomial expected\n");
	printf("%3s %7s %9s\n", "k", "obs", "expected");
	maxc = 1;
	k = -1;
	while (++k <= K)
		if (c->hist[k] > maxc)
			maxc = c->hist[k];
	k = -1;
	while (++k <= K)
	{
		printf("%3d %7ld %9.1f ", k, c->hist[k], expected(c, k));
		bar((int)(40.0 * c->hist[k] / maxc + 0.5));
	}
}

void	print_stats(t_coin *c)
{
	double	ph;
	double	sd;
	double	z;

	ph = (double)c->heads / c->n;
	sd = sqrt(c->n * c->p * (1 - c->p));
	z = (c->heads - c->n * c->p) / sd;
	printf("\nHeads=%ld  Tails=%ld  p_hat=%.4f\n", c->heads, c->n - c->heads,
		ph);
	printf("Expected heads=%.1f  SD=%.2f  z=%.3f\n", c->n * c->p, sd, z);
	printf("H0: P(H)=%.3f at alpha=0.05 -> ", c->p);
	if (fabs(z) < 1.96)
		printf("fail to reject\n");
	else
		printf("REJECT\n");
}
