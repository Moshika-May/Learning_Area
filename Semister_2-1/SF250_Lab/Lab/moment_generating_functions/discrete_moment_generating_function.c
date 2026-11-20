#include "discrete.h"

static int	usage(char *prog)
{
	fprintf(stderr, "usage: %s bernoulli p | binomial n p | ", prog);
	fprintf(stderr, "poisson lambda\n");
	fprintf(stderr, "e.g.   %s binomial 1000000000 0.3\n", prog);
	return (1);
}

static int	check(t_dist *d)
{
	if (!d->poisson && !(d->p > 0 && d->p < 1))
	{
		fprintf(stderr, "need 0<p<1\n");
		return (1);
	}
	if (d->poisson && !(d->lam > 0))
	{
		fprintf(stderr, "need lambda>0\n");
		return (1);
	}
	return (0);
}

static int	parse(t_dist *d, int ac, char **av)
{
	char	*name;

	name = "";
	if (ac > 1)
		name = av[1];
	if (!strcmp(name, "bernoulli") && ac == 3)
	{
		d->n = 1;
		d->p = atof(av[2]);
	}
	else if (!strcmp(name, "binomial") && ac == 4)
	{
		d->n = strtoull(av[2], NULL, 10);
		d->p = atof(av[3]);
	}
	else if (!strcmp(name, "poisson") && ac == 3)
	{
		d->poisson = 1;
		d->lam = atof(av[2]);
	}
	else
		return (usage(av[0]));
	return (check(d));
}

int	main(int ac, char **av)
{
	t_dist	d;
	double	mean;
	double	var;

	memset(&d, 0, sizeof(d));
	if (parse(&d, ac, av))
		return (1);
	mean = d.lam;
	var = d.lam;
	if (!d.poisson)
	{
		mean = d.n * d.p;
		var = d.n * d.p * (1 - d.p);
	}
	print_intro(&d);
	print_table(&d);
	print_moments(&d, mean, var);
	plots(&d, mean, var);
	return (0);
}
