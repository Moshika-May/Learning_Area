/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mgf_continuous.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Moshika <moshika@localhost>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/20 14:40:00 by Moshika           #+#    #+#             */
/*   Updated: 2026/11/20 14:40:00 by Moshika          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "cont.h"

static int	usage(char *prog)
{
	fprintf(stderr, "usage: %s uniform a b [N] | exponential lambda [N] | ",
		prog);
	fprintf(stderr, "gaussian mu sigma [N]\n");
	fprintf(stderr, "e.g.   %s gaussian 1 2 100000000\n", prog);
	return (1);
}

static int	pick2(t_cont *c, char **av)
{
	if (!strcmp(av[1], "uniform"))
	{
		c->kind = 'u';
		c->a = atof(av[2]);
		c->b = atof(av[3]);
		return (4);
	}
	c->kind = 'g';
	c->mu = atof(av[2]);
	c->sg = atof(av[3]);
	return (4);
}

static int	pick(t_cont *c, int ac, char **av)
{
	char	*name;

	name = "";
	if (ac > 1)
		name = av[1];
	if (!strcmp(name, "exponential") && ac >= 3)
	{
		c->kind = 'e';
		c->lam = atof(av[2]);
		return (3);
	}
	if ((!strcmp(name, "uniform") || !strcmp(name, "gaussian")) && ac >= 4)
		return (pick2(c, av));
	return (0);
}

static int	parse(t_cont *c, int ac, char **av)
{
	int	na;

	na = pick(c, ac, av);
	if (!na)
		return (usage(av[0]));
	c->n = 1000000;
	if (ac > na)
		c->n = strtoull(av[na], NULL, 10);
	c->n += c->n & 1;
	if (!c->n)
		c->n = 2;
	return (check_params(c));
}

int	main(int ac, char **av)
{
	t_cont	c;

	memset(&c, 0, sizeof(c));
	if (parse(&c, ac, av))
		return (1);
	setup(&c);
	print_title(&c);
	print_intro(&c);
	print_table(&c);
	print_moments(&c);
	plots(&c);
	return (0);
}
