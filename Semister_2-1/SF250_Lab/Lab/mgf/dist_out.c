/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dist_out.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Moshika <moshika@localhost>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/20 14:40:00 by Moshika           #+#    #+#             */
/*   Updated: 2026/11/20 14:40:00 by Moshika          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "dist.h"

static const double	g_ts[7] = {-1, -.5, -.1, 0, .1, .5, .9};

void	print_intro(t_dist *d)
{
	const char	*name;

	if (d->poisson)
		printf("Poisson(lambda=%g)\n", d->lam);
	else
	{
		name = "Binomial";
		if (d->n == 1)
			name = "Bernoulli";
		printf("%s(n=%zu, p=%g)\n", name, d->n, d->p);
	}
	printf("M(t) = E[e^{tX}] = ");
	if (d->poisson)
		printf("exp(lambda (e^t - 1))\n");
	else
		printf("(1-p+p e^t)^n\n");
	printf("\n%8s %16s %16s %12s   (K = log M)\n", "t", "K closed",
		"K brute-sum", "|diff|");
}

void	print_table(t_dist *d)
{
	int		i;
	double	a;
	double	b;

	i = -1;
	while (++i < 7)
	{
		a = kclosed(d, g_ts[i]);
		b = knum(d, g_ts[i]);
		printf("%8.2f %16.8g %16.8g %12.3g\n", g_ts[i], a, b, fabs(a - b));
	}
}

void	print_moments(t_dist *d, double mean, double var)
{
	double	h;
	double	k1;
	double	k0;

	h = 1e-3;
	k1 = kclosed(d, h);
	k0 = kclosed(d, -h);
	printf("\nmoments from derivatives of K at t=0 ");
	printf("(K'(0)=mean, K''(0)=var):\n");
	printf("  mean  numeric %.8g  theory %.8g\n", (k1 - k0) / (2 * h), mean);
	printf("  var   numeric %.8g  theory %.8g\n", (k1 - 2 * kclosed(d, 0) + k0)
		/ (h * h), var);
}
