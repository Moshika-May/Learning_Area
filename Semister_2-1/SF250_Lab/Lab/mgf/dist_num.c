/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dist_num.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Moshika <moshika@localhost>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/20 14:40:00 by Moshika           #+#    #+#             */
/*   Updated: 2026/11/20 14:40:00 by Moshika          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "dist.h"

static void	tilt(t_dist *d, double t, double *mu, double *sd)
{
	double	q;

	if (d->poisson)
	{
		*mu = d->lam * exp(t);
		*sd = sqrt(*mu);
		return ;
	}
	q = exp(log(d->p) + t - lae(log1p(-d->p), log(d->p) + t));
	*mu = d->n * q;
	*sd = sqrt(d->n * q * (1 - q));
}

static void	bounds(t_dist *d, double t, size_t *lo, size_t *hi)
{
	double	mu;
	double	sd;
	double	fhi;

	tilt(d, t, &mu, &sd);
	*lo = (size_t)fmax(0, mu - 12 * sd - 5);
	fhi = mu + 12 * sd + 5;
	*hi = (size_t)fhi;
	if (!d->poisson && fhi > (double)d->n)
		*hi = d->n;
}

double	knum(t_dist *d, double t)
{
	size_t	r[2];
	size_t	k;
	double	m;
	double	s;

	bounds(d, t, &r[0], &r[1]);
	m = -INFINITY;
	k = r[0] - 1;
	while (++k <= r[1])
		m = fmax(m, logpmf(d, k) + t * k);
	s = 0;
	k = r[0] - 1;
	while (++k <= r[1])
		s += exp(logpmf(d, k) + t * k - m);
	return (m + log(s));
}
