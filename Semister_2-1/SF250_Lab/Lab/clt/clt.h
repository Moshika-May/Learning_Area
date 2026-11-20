#ifndef CLT_H
# define CLT_H

# include <math.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <time.h>

# define B 16
# define W 40

typedef struct s_clt
{
	int				ex;
	long			n;
	long			reps;
	long			h[B];
	double			mu;
	double			sd;
	double			s1;
	double			s2;
	double			s3;
	unsigned int	seed;
}	t_clt;

double	phi(double z);
void	simulate(t_clt *c);
void	print_hist(t_clt *c);
void	print_stats(t_clt *c);

#endif
