/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_assign_index.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 14:11:38 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 14:11:39 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

void	ft_assign_index(t_stack *a)
{
	t_stack	*tmp;

	int (i), size, *arr;
	size = ft_lstsize(a);
	arr = malloc(sizeof(int) * size);
	if (!arr)
		ft_error();
	tmp = a;
	i = 0;
	while (tmp)
	{
		arr[i++] = tmp->nbr;
		tmp = tmp->next;
	}
	ft_sort_array(arr, size);
	tmp = a;
	while (tmp)
	{
		i = 0;
		while (arr[i] != tmp->nbr)
			i++;
		tmp->index = i;
		tmp = tmp->next;
	}
	free(arr);
}
