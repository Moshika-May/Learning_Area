/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   clt.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Moshika <moshika@localhost>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/20 14:40:00 by Moshika           #+#    #+#             */
/*   Updated: 2026/11/20 14:40:00 by Moshika          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "clt.h"

static int	parse(t_clt *c, int ac, char **av)
{
	c->ex = ac > 1 && !strcmp(av[1], "exp");
	c->n = 30;
	c->reps = 10000;
	c->seed = (unsigned int)time(NULL);
	if (ac > 2)
		c->n = atol(av[2]);
	if (ac > 3)
		c->reps = atol(av[3]);
	if (ac > 4)
		c->seed = (unsigned int)atol(av[4]);
	if ((ac > 1 && !c->ex && strcmp(av[1], "uniform")) || c->n < 1
		|| c->reps < 1)
	{
		fprintf(stderr, "usage: %s [uniform|exp] [n>=1] [reps>=1] [seed]\n",
			av[0]);
		return (1);
	}
	return (0);
}

static const char	*pop_name(t_clt *c)
{
	if (c->ex)
		return ("Exp(1)");
	return ("Uniform(0,1)");
}

static void	print_head(t_clt *c)
{
	printf("== CLT: population=%s, ", pop_name(c));
	printf("sample size n=%ld, repetitions=%ld, ", c->n, c->reps);
	printf("seed=%u ==\n", c->seed);
	printf("Histogram of z = (xbar - mu)/(sigma/sqrt n): ");
	printf("observed (#) vs Normal(0,1) expected\n");
	printf("%11s %7s %9s\n", "z range", "obs", "expected");
}

int	main(int ac, char **av)
{
	t_clt	c;

	if (parse(&c, ac, av))
		return (1);
	srand(c.seed);
	c.mu = 0.5;
	c.sd = sqrt(1.0 / 12);
	if (c.ex)
	{
		c.mu = 1;
		c.sd = 1;
	}
	memset(c.h, 0, sizeof(c.h));
	simulate(&c);
	print_head(&c);
	print_hist(&c);
	print_stats(&c);
	return (0);
}
