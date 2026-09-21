/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_push_swap.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 14:59:18 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 14:59:22 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

//this functions decides which sort should the stack goes to 
static void	ft_passing_to_sorting(t_stack **a, t_stack **b)
{
	int	size;

	size = ft_lstsize(*a);
	if (size <= 5)
	{
		if (size == 5)
			ft_sort_five(a, b);
		else if (size == 4)
			ft_sort_four(a, b);
		else if (size == 3)
			ft_sort_three(a);
		else if (size == 2)
			ft_sort_two(a);
	}
	else
		ft_big_sort(a, b);
}

static void	ft_push_swap(int ac, char **av)
{
	t_stack	*a;
	t_stack	*b;

	a = ft_parsing(ac, av);
	b = NULL;
	if (ft_lstsize(a) <= 1 || ft_checksorted(a))
	{
		ft_lstclear(&a);
		return ;
	}
	ft_assign_index(a);
	ft_passing_to_sorting(&a, &b);
	b = NULL;
	ft_lstclear(&a);
}

int	main(int ac, char **av)
{
	int	i;

	i = 0;
	if (ac < 2)
		return (0);
	if (av[1][i] == '\0')
		ft_error();
	if (!ft_just_spaces(av[1]))
		ft_error();
	ft_push_swap(ac, av);
	return (0);
}
