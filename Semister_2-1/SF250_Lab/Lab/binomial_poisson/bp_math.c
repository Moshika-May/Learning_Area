/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bp_math.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Moshika <moshika@localhost>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/20 14:40:00 by Moshika           #+#    #+#             */
/*   Updated: 2026/11/20 14:40:00 by Moshika          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bp.h"

double	lbin(long n, long r, double p)
{
	return (lgamma(n + 1.0) - lgamma(r + 1.0) - lgamma(n - r + 1.0) + r * log(p)
		+ (n - r) * log1p(-p));
}

double	lpoi(double l, long r)
{
	return (r * log(l) - l - lgamma(r + 1.0));
}

void	simulate(t_bp *b)
{
	long	i;
	long	j;
	long	x;

	i = -1;
	b->s1 = 0;
	b->s2 = 0;
	while (++i < b->samples)
	{
		x = 0;
		j = -1;
		while (++j < b->n)
			if (rand() / (RAND_MAX + 1.0) < b->p)
				x++;
		b->s1 += x;
		b->s2 += (double)x * x;
		if (x <= b->top)
			b->h[x]++;
	}
}
