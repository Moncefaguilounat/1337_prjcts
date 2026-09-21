/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_operations2.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 14:47:51 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 14:47:52 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

// rb (rotate b) : shift up all elements by one
// the first one becomes the last one
void	ft_rb(t_stack **b, int print)
{
	t_stack	*tmp;

	if (!*b || !(*b)->next)
		return ;
	tmp = *b;
	*b = ft_lstlast(*b);
	(*b)->next = tmp;
	*b = tmp->next;
	tmp->next = NULL;
	if (print)
		write (1, "rb\n", 3);
}

// ss : sa and sb
void	ft_ss(t_stack **a, t_stack **b, int print)
{
	if ((!*b || !(*b)->next) || (!*a || !(*a)->next))
		return ;
	ft_sb(b, 0);
	ft_sa(a, 0);
	if (print)
		write (1, "ss\n", 3);
}

// pb (push b) : take the first 
// element at the top of a and put it 
// at the top of b. Do nothing if a is empty.
void	ft_pb(t_stack **stack_a, t_stack **stack_b, int print)
{
	t_stack	*tmp;

	if (!*stack_a)
		return ;
	tmp = *stack_b;
	*stack_b = *stack_a;
	*stack_a = (*stack_a)->next;
	(*stack_b)->next = tmp;
	if (print)
		write(1, "pb\n", 3);
}
