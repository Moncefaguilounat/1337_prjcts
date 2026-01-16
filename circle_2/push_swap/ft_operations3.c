/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_operations3.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 14:50:04 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 14:50:05 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

//rr : ra and rb in the same time
void	ft_rr(t_stack **a, t_stack **b, int print)
{
	if ((!*a || !((*a)->next)) || (!*b || !((*b)->next)))
		return ;
	ft_ra(a, 0);
	ft_rb(b, 0);
	if (print)
		write(1, "rr\n", 3);
}

// rrb (reverse rotate b) , shift down all 
// elements by 1 , the las one becomes the first one
void	ft_rrb(t_stack **b, int print)
{
	t_stack	*tmp;
	int		i;

	if (!*b || !(*b)->next)
		return ;
	tmp = *b;
	i = 0;
	while ((*b)->next)
	{
		*b = (*b)->next;
		i++;
	}
	(*b)->next = tmp;
	while (i-- > 1)
		tmp = tmp->next;
	tmp->next = NULL;
	if (print)
		write(1, "rrb\n", 4);
}

// rrr rra and rrb in the same time
void	ft_rrr(t_stack **a, t_stack **b, int print)
{
	if ((!*a || !((*a)->next)) || (!*b || !((*b)->next)))
		return ;
	ft_rra(a, 0);
	ft_rrb(b, 0);
	if (print)
		write(1, "rrr\n", 4);
}
