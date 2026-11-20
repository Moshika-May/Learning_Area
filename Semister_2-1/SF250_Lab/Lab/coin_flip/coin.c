#include "coin.h"

static int	parse(t_coin *c, int ac, char **av)
{
	c->n = 1000;
	c->p = 0.5;
	c->seed = (unsigned int)time(NULL);
	if (ac > 1)
		c->n = atol(av[1]);
	if (ac > 2)
		c->p = atof(av[2]);
	if (ac > 3)
		c->seed = (unsigned int)atol(av[3]);
	if (c->n < K || c->p <= 0 || c->p >= 1)
	{
		fprintf(stderr, "usage: %s [N>=%d] [0<p<1] [seed]\n", av[0], K);
		return (1);
	}
	return (0);
}

static void	print_head(t_coin *c)
{
	printf("== Coin flip simulation: N=%ld, P(H)=%.3f, seed=%u ==\n\n", c->n,
		c->p, c->seed);
	printf("Convergence of running proportion (Law of Large Numbers)\n");
	printf("%9s %7s  0%*s1\n", "n", "p_hat", W - 1, "");
}

int	main(int ac, char **av)
{
	t_coin	c;

	memset(&c, 0, sizeof(c));
	if (parse(&c, ac, av))
		return (1);
	srand(c.seed);
	print_head(&c);
	simulate(&c);
	print_hist(&c);
	print_stats(&c);
	return (0);
}
