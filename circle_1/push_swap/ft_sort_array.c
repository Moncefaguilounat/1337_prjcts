/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_array.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 15:01:12 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 15:01:15 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

void	ft_sort_array(int *tab, int size)
{
	int (i), j, swp, swpd;
	i = 0;
	while (i < size - 1)
	{
		swpd = 0;
		j = 0;
		while (j < size - 1 - i)
		{
			if (tab[j] > tab[j + 1])
			{
				swp = tab[j];
				tab[j] = tab[j + 1];
				tab[j + 1] = swp;
				swpd = 1;
			}
			j++;
		}
		if (swpd == 0)
			break ;
		i++;
	}
}
