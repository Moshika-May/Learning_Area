#ifndef CONT_H
# define CONT_H

# include <math.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include "plot.h"

typedef struct s_cont
{
	char	kind;
	size_t	n;
	double	a;
	double	b;
	double	lam;
	double	mu;
	double	sg;
	double	mean;
	double	var;
	double	unit;
}	t_cont;

double	kclosed(t_cont *c, double t);
double	logpdf(t_cont *c, double x);
void	setup(t_cont *c);
int		check_params(t_cont *c);
double	knum(t_cont *c, double t);
void	print_title(t_cont *c);
void	print_intro(t_cont *c);
void	print_table(t_cont *c);
void	print_moments(t_cont *c);
void	plots(t_cont *c);

#endif
