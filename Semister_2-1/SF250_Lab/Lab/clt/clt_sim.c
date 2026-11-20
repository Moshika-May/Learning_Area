/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   clt_sim.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Moshika <moshika@localhost>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/20 14:40:00 by Moshika           #+#    #+#             */
/*   Updated: 2026/11/20 14:40:00 by Moshika          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "clt.h"

double	phi(double z)
{
	return (0.5 * erfc(-z / M_SQRT2));
}

static double	u(void)
{
	return ((rand() + 1.0) / (RAND_MAX + 2.0));
}

static double	zscore(t_clt *c)
{
	long	i;
	double	m;

	m = 0;
	i = -1;
	while (++i < c->n)
	{
		if (c->ex)
			m += -log(u());
		else
			m += u();
	}
	return ((m / c->n - c->mu) / (c->sd / sqrt((double)c->n)));
}

void	simulate(t_clt *c)
{
	long	r;
	double	z;
	int		b;

	c->s1 = 0;
	c->s2 = 0;
	c->s3 = 0;
	r = -1;
	while (++r < c->reps)
	{
		z = zscore(c);
		c->s1 += z;
		c->s2 += z * z;
		c->s3 += z * z * z;
		b = (int)floor((z + 4) * 2);
		if (b >= 0 && b < B)
			c->h[b]++;
	}
}
