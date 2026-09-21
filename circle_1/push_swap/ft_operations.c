/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_operations.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 14:51:17 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 14:51:21 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

// ra (rotate a) : shift up all elements by one ...
// the first one becomes the last one
void	ft_ra(t_stack **a, int print)
{
	t_stack	*tmp;

	if (!*a || !(*a)->next)
		return ;
	tmp = *a;
	*a = ft_lstlast(*a);
	(*a)->next = tmp;
	*a = tmp->next;
	tmp->next = NULL;
	if (print)
		write (1, "ra\n", 3);
}

// swap the first two elements in a
// do nothing if there is no enough elements
void	ft_sa(t_stack **a, int print)
{
	t_stack	*tmp;

	if (!*a || !(*a)->next)
		return ;
	tmp = *a;
	*a = (*a)->next;
	tmp->next = (*a)->next;
	(*a)->next = tmp;
	if (print)
		write (1, "sa\n", 3);
}

// pa (push a) , push the top element of 
// stack b into a , do nothing if "b" is empty
void	ft_pa(t_stack **a, t_stack **b, int print)
{
	t_stack	*tmp;

	if (!*b)
		return ;
	tmp = *a;
	*a = *b;
	*b = (*b)->next;
	(*a)->next = tmp;
	if (print)
		write (1, "pa\n", 3);
}

// rra (reverse rotate a) , shift down 
// all elements by 1 , the last one becomes
// the first one
void	ft_rra(t_stack **a, int print)
{
	t_stack	*tmp;
	int		i;

	if (!*a || !(*a)->next)
		return ;
	tmp = *a;
	i = 0;
	while ((*a)->next)
	{
		*a = (*a)->next;
		i++;
	}
	(*a)->next = tmp;
	while (i-- > 1)
		tmp = tmp->next;
	tmp->next = NULL;
	if (print)
		write(1, "rra\n", 4);
}

// swap the first two elements in b
// do nothing if there is no enough elements
void	ft_sb(t_stack **b, int print)
{
	t_stack	*tmp;

	if (!*b || !(*b)->next)
		return ;
	tmp = *b;
	*b = (*b)->next;
	tmp->next = (*b)->next;
	(*b)->next = tmp;
	if (print)
		write (1, "sb\n", 3);
}
