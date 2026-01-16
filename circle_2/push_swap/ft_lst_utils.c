/* ************************************************************************** */
/*																			  */
/*                                                        :::      ::::::::   */
/*   ft_lst_utils.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 14:15:43 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 14:15:44 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

//this function returns the min nbr found in the stack
int	ft_min(t_stack *lst)
{
	int	i;

	i = lst->nbr;
	lst = lst->next;
	while (lst)
	{
		if (i > lst->nbr)
			i = lst->nbr;
		lst = lst->next;
	}
	return (i);
}

//this function returns the max nbr in the stack
int	ft_max(t_stack *lst)
{
	int	i;

	i = lst->nbr;
	lst = lst->next;
	while (lst)
	{
		if (i < lst->nbr)
			i = lst->nbr;
		lst = lst->next;
	}
	return (i);
}

//this function returns the size of the lst
int	ft_lstsize(t_stack *lst)
{
	int	i;

	i = 0;
	while (lst)
	{
		lst = lst->next;
		i++;
	}
	return (i);
}

//this function returns the last node in the list
t_stack	*ft_lstlast(t_stack *lst)
{
	while (lst->next)
		lst = lst->next;
	return (lst);
}

//this function finds the index of n in the given stack
int	ft_find_index(t_stack *s, int n)
{
	int	i;

	i = 0;
	while (n != s->nbr)
	{
		i++;
		s = s->next;
	}
	return (i);
}
