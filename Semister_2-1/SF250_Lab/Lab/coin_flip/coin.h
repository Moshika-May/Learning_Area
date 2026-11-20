#ifndef COIN_H
# define COIN_H

# include <math.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <time.h>

# define K 10
# define NC 20
# define W 50

typedef struct s_coin
{
	long			n;
	long			heads;
	long			groups;
	long			hist[K + 1];
	double			p;
	unsigned int	seed;
}	t_coin;

void	simulate(t_coin *c);
void	print_hist(t_coin *c);
void	print_stats(t_coin *c);

#endif
