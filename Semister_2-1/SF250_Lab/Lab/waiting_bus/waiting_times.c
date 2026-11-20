/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   waiting_times.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Moshika <moshika@localhost>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/20 14:40:00 by Moshika           #+#    #+#             */
/*   Updated: 2026/11/20 14:40:00 by Moshika          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BINS 30

static double	u(void)
{
	return ((rand() + 1.0) / (RAND_MAX + 2.0));
}

static void	hist(const char *name, const int *h, double w, double mean)
{
	int	max;
	int	i;
	int	j;

	max = 1;
	i = -1;
	while (++i < BINS)
		if (h[i] > max)
			max = h[i];
	printf("\n%s  (mean = %.3f)\n", name, mean);
	i = -1;
	while (++i < BINS)
	{
		printf("%6.2f-%6.2f |", i * w, (i + 1) * w);
		j = -1;
		while (++j < h[i] * 50 / max)
			putchar('#');
		printf(" %d\n", h[i]);
	}
}

static void	add(int *h, double x, double w)
{
	int	i;

	i = (int)(x / w);
	if (i >= BINS)
		i = BINS - 1;
	h[i]++;
}

static void	sim(double period, int n, int h[2][BINS], double sum[2])
{
	int		i;
	double	a;
	double	b;

	i = -1;
	sum[0] = 0;
	sum[1] = 0;
	srand(250);
	while (++i < n)
	{
		a = period * u();
		b = -period * log(u());
		sum[0] += a;
		sum[1] += b;
		add(h[0], a, period / 10);
		add(h[1], b, period / 10);
	}
}

int	main(void)
{
	double	period;
	int		n;
	int		h[2][BINS];
	double	sum[2];

	printf("Average bus interval T (minutes, e.g. 15): ");
	if (scanf("%lf", &period) != 1 || period <= 0)
		return (1);
	printf("Number of samples (e.g. 100000): ");
	if (scanf("%d", &n) != 1 || n <= 0)
		return (1);
	memset(h, 0, sizeof(h));
	sim(period, n, h, sum);
	hist("1) Regular buses: Uniform[0,T]", h[0], period / 10, sum[0] / n);
	printf("   theory T/2 = %.3f\n", period / 2);
	hist("2) Random buses: Exponential(1/T)", h[1], period / 10, sum[1] / n);
	printf("   theory T = %.3f   (last bar includes waits >= 3T)\n", period);
	return (0);
}
