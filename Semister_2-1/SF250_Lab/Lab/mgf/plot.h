#ifndef PLOT_H
# define PLOT_H

# include <math.h>
# include <stdio.h>
# include <string.h>

# define PW 70
# define PH 16

typedef double	(*t_fn)(double, void *);

typedef struct s_curve
{
	const char	*title;
	t_fn		f;
	void		*ctx;
	double		lo;
	double		hi;
}	t_curve;

typedef struct s_plot
{
	double	y[PW];
	char	g[PH][PW + 1];
	double	ymin;
	double	ymax;
}	t_plot;

void	plot(t_curve *c);

#endif
