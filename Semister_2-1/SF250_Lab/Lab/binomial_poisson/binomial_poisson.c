#include "binomial_poisson.h"

static int	parse(t_bp *b, int ac, char **av)
{
	b->n = 100;
	b->p = 0.05;
	b->samples = 100000;
	b->seed = (unsigned)time(NULL);
	if (ac > 1)
		b->n = atol(av[1]);
	if (ac > 2)
		b->p = atof(av[2]);
	if (ac > 3)
		b->samples = atol(av[3]);
	if (ac > 4)
		b->seed = (unsigned)atol(av[4]);
	if (b->n < 1 || b->samples < 1 || b->p <= 0 || b->p >= 1)
	{
		fprintf(stderr, "usage: %s [n>=1] [0<p<1] [samples>=1] [seed]\n",
			av[0]);
		return (1);
	}
	return (0);
}

int	main(int ac, char **av)
{
	t_bp	b;

	if (parse(&b, ac, av))
		return (1);
	srand(b.seed);
	b.lam = b.n * b.p;
	b.top = (long)ceil(b.lam + 6 * sqrt(b.lam) + 5);
	if (b.top > b.n)
		b.top = b.n;
	b.h = calloc(b.top + 1, sizeof(long));
	simulate(&b);
	printf("== Binomial B(n=%ld, p=%g) ", b.n, b.p);
	printf("vs Poisson Po(lambda=np=%g), ", b.lam);
	printf("%ld samples, seed=%u ==\n", b.samples, b.seed);
	print_table(&b);
	print_stats(&b);
	free(b.h);
	return (0);
}
