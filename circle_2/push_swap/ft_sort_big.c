/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_big.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 16:26:59 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 16:27:02 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

static void	ft_final_rotate(t_stack **a)
{
	int	min_idx;
	int	elem_pos;

	min_idx = ft_min_index(*a);
	elem_pos = ft_find_position(*a, min_idx);
	if (elem_pos <= (ft_lstsize(*a) / 2))
	{
		while ((*a)->index != min_idx)
			ft_ra(a, 1);
	}
	else
	{
		while ((*a)->index != min_idx)
			ft_rra(a, 1);
	}
}

static void	ft_push_back(t_stack **a, t_stack **b)
{
	int	max;
	int	elem_pos;

	while (*b)
	{
		max = ft_max_index(*b);
		elem_pos = ft_find_position(*b, max);
		if (elem_pos <= (ft_lstsize(*b) / 2))
		{
			while ((*b)->index != max)
				ft_rb(b, 1);
		}
		else
		{
			while ((*b)->index != max)
				ft_rrb(b, 1);
		}
		ft_pa(a, b, 1);
	}
	ft_final_rotate(a);
}

void	ft_big_sort(t_stack **a, t_stack **b)
{
	int (i), chunk_size;
	if (ft_lstsize(*a) <= 100)
		chunk_size = 17;
	else
		chunk_size = 40;
	i = 0;
	while (ft_lstsize(*a))
	{
		if ((*a)->index <= i)
		{
			ft_pb(a, b, 1);
			ft_rb(b, 1);
			i++;
		}
		else if ((*a)->index <= i + chunk_size)
		{
			ft_pb(a, b, 1);
			i++;
		}
		else
			ft_ra(a, 1);
	}
	ft_push_back(a, b);
}
