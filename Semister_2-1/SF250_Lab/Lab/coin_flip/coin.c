// Coin flip simulation. Build: gcc -O2 -o coin coin.c -lm
// Run:   ./coin [N=1000] [p_head=0.5] [seed=time]
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define K 10  // flips per group for the binomial histogram
#define NC 20 // checkpoints on the convergence plot
#define W 50  // plot width (columns)

static void	bar(char c, int n)
{
	while (n-- > 0)
		putchar(c);
}

int	main(int argc, char **argv)
{
	long		n;
	double		p;
	unsigned	seed;
	long		heads = 0, hist[K + 1] = {0}, groups = 0;
	int			gh = 0, ci;
	int			h;
	double		ph;
	int			col = (int)(ph * (W - 1) + 0.5), mid;
	double		maxc;
	double		e;
	double		ph = (double)heads / n, sd;
	double		z = (heads - n * p) / sd, ci_w;

	n = argc > 1 ? atol(argv[1]) : 1000;
	p = argc > 2 ? atof(argv[2]) : 0.5;
	seed = argc > 3 ? (unsigned)atol(argv[3]) : (unsigned)time(NULL);
	if (n < K || p <= 0 || p >= 1)
	{
		fprintf(stderr, "usage: %s [N>=%d] [0<p<1] [seed]\n", argv[0], K);
		return (1);
	}
	srand(seed);
	gh = 0, ci = 1;
	printf("== Coin flip simulation: N=%ld, P(H)=%.3f, seed=%u ==\n\n", n, p,
		seed);
	printf("Convergence of running proportion (Law of Large Numbers)\n");
	printf("%9s %7s  0%*s1\n", "n", "p_hat", W - 1, "");
	for (long i = 1; i <= n; i++)
	{
		h = rand() / (RAND_MAX + 1.0) < p;
		heads += h;
		gh += h;
		if (i % K == 0)
		{
			hist[gh]++;
			groups++;
			gh = 0;
		}
		while (ci <= NC && i >= (long)ceil(pow((double)n, (double)ci / NC)))
		{
			ph = (double)heads / i;
			col = (int)(ph  (W - 1) + 0.5), mid = (int)(p * (W - 1) + 0.5);
			printf("%9ld %7.4f  ", i, ph);
			for (int x = 0; x < W; x++)
				putchar(x == col ? '*' : x == mid ? '|' : ' ');
			putchar('\n');
			ci++;
		}
	}
	printf("\nHeads per group of %d flips: observed (#) vs binomial expected\n",
		K);
	printf("%3s %7s %9s\n", "k", "obs", "expected");
	maxc = 1;
	for (int k = 0; k <= K; k++)
		if (hist[k] > maxc)
			maxc = hist[k];
	for (int k = 0; k <= K; k++)
	{
		e = groups * tgamma(K + 1) / (tgamma(k + 1) * tgamma(K - k + 1))
			* pow(p, k) * pow(1 - p, K - k);
		printf("%3d %7ld %9.1f ", k, hist[k], e);
		bar('#', (int)(40.0 * hist[k] / maxc + 0.5));
		putchar('\n');
	}
	ph = (double)heads / n, sd = sqrt(n * p * (1 - p));
	z = (heads - n  p) / sd, ci_w = 1.96 * sqrt(ph * (1 - ph) / n);
	printf("\nHeads=%ld  Tails=%ld  p_hat=%.4f\n", heads, n - heads, ph);
	printf("Expected heads=%.1f  SD=%.2f  z=%.3f  chi2(df=1)=%.3f (crit 3.841)\n",
		n * p, sd, z, z * z);
	printf("95%% CI for p: [%.4f, %.4f]\n", ph - ci_w, ph + ci_w);
	printf("H0: P(H)=%.3f at alpha=0.05 -> %s\n", p,
		fabs(z) < 1.96 ? "fail to reject" : "REJECT");
	return (0);
}
