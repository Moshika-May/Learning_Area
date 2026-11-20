#ifndef DISCRETE_H
# define DISCRETE_H

# include <math.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include "plot.h"

typedef struct s_dist
{
	int		poisson;
	size_t	n;
	double	p;
	double	lam;
}	t_dist;

double	lae(double a, double b);
double	kclosed(t_dist *d, double t);
double	logpmf(t_dist *d, size_t k);
double	knum(t_dist *d, double t);
void	print_intro(t_dist *d);
void	print_table(t_dist *d);
void	print_moments(t_dist *d, double mean, double var);
void	plots(t_dist *d, double mean, double var);

#endif
