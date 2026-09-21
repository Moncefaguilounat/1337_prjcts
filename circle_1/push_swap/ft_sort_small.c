/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_small.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 15:14:32 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 15:14:33 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

//this function sorts the stack if there is five elements in it
void	ft_sort_five(t_stack **a, t_stack **b)
{
	int	min;
	int	min_idx;

	min = ft_min(*a);
	min_idx = ft_find_index(*a, min);
	if (min_idx > (5 / 2))
	{
		while (min != (*a)->nbr)
			ft_rra(a, 1);
	}
	else
		while (min != (*a)->nbr)
			ft_ra(a, 1);
	ft_pb(a, b, 1);
	ft_sort_four(a, b);
	ft_pa(a, b, 1);
}

//this function sorts the stack if there is four elements in it
void	ft_sort_four(t_stack **a, t_stack **b)
{
	int	min;
	int	min_idx;

	min = ft_min(*a);
	min_idx = ft_find_index(*a, min);
	if (min_idx > (4 / 2))
	{
		while (min != (*a)->nbr)
			ft_rra(a, 1);
	}
	else if (min_idx == 1 || min_idx == 2)
	{
		while (min != (*a)->nbr)
			ft_ra(a, 1);
	}
	ft_pb(a, b, 1);
	ft_sort_three(a);
	ft_pa(a, b, 1);
}

//this function sorts the stack if there is only three elements in it
void	ft_sort_three(t_stack **a)
{
	int	min;
	int	max;

	min = ft_min(*a);
	max = ft_max(*a);
	if (min == (*a)->nbr)
	{
		ft_rra(a, 1);
		ft_sa(a, 1);
	}
	else if (max == (*a)->nbr)
	{
		ft_ra(a, 1);
		if (!ft_checksorted(*a))
			ft_sa(a, 1);
	}
	else
	{
		if (ft_find_index(*a, max) == 1)
			ft_rra(a, 1);
		else
			ft_sa(a, 1);
	}
}

//this function is supposed to sort
//the stack if there is only two elements in it
void	ft_sort_two(t_stack **a)
{
	if ((*a)->nbr > (*a)->next->nbr)
		ft_sa(a, 1);
}
