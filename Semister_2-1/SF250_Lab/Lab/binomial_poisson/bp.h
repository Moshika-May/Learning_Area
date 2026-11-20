/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bp.h                                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Moshika <moshika@localhost>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/11/20 14:40:00 by Moshika           #+#    #+#             */
/*   Updated: 2026/11/20 14:40:00 by Moshika          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef BP_H
# define BP_H

# include <math.h>
# include <stdio.h>
# include <stdlib.h>
# include <time.h>

# define W 40

typedef struct s_bp
{
	long			n;
	long			samples;
	long			top;
	long			*h;
	double			p;
	double			lam;
	double			s1;
	double			s2;
	double			tv;
	unsigned int	seed;
}	t_bp;

double			lbin(long n, long r, double p);
double			lpoi(double l, long r);
void			simulate(t_bp *b);
void			print_table(t_bp *b);
void			print_stats(t_bp *b);

#endif
