/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   clt_print.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Moshika <moshika@localhost>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/20 14:40:00 by Moshika           #+#    #+#             */
/*   Updated: 2026/11/20 14:40:00 by Moshika          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "clt.h"

static long	max_count(t_clt *c)
{
	long	mx;
	int		i;

	mx = 1;
	i = -1;
	while (++i < B)
		if (c->h[i] > mx)
			mx = c->h[i];
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

void	print_hist(t_clt *c)
{
	int		i;
	long	mx;
	double	lo;
	double	e;

	mx = max_count(c);
	i = -1;
	while (++i < B)
	{
		lo = -4 + 0.5 * i;
		e = c->reps * (phi(lo + 0.5) - phi(lo));
		printf("[%+.1f,%+.1f) %7ld %9.1f ", lo, lo + 0.5, c->h[i], e);
		bar(c->h[i], mx);
	}
}

void	print_stats(t_clt *c)
{
	double	m;
	double	v;
	double	sk;
	double	pop;

	m = c->s1 / c->reps;
	v = c->s2 / c->reps - m * m;
	sk = (c->s3 / c->reps - 3 * m * v - m * m * m) / pow(v, 1.5);
	pop = 0;
	if (c->ex)
		pop = 2;
	printf("\nmean(z)=%+.4f (theory 0)  var(z)=%.4f (theory 1)  ", m, v);
	printf("skewness=%+.4f ", sk);
	printf("(theory %+.4f = pop. skew/sqrt n -> 0)\n", pop
		/ sqrt((double)c->n));
	printf("Tip: try n=1, 5, 30, 200 with exp to watch the skew vanish.\n");
}
