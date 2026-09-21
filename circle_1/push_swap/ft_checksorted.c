/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_checksorted.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 14:21:27 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 14:21:29 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

int	ft_checksorted(t_stack *a)
{
	int	i;

	i = a->nbr;
	while (a->next)
	{
		a = a->next;
		if (i > a->nbr)
			return (0);
		i = a->nbr;
	}
	return (1);
}
