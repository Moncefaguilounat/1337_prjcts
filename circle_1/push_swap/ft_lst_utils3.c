/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lst_utils3.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 13:54:16 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 13:54:18 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

t_stack	*ft_lstnew(int *content)
{
	t_stack	*res;

	res = malloc(sizeof(t_stack));
	if (!res)
		ft_error();
	res->nbr = *content;
	res->next = NULL;
	return (res);
}

void	ft_lstclear(t_stack **lst)
{
	t_stack	*current;
	t_stack	*d;

	if (!lst || !*lst)
		return ;
	current = *lst;
	while (current)
	{
		d = current;
		current = current->next;
		free(d);
	}
	*lst = NULL;
}

void	ft_lstadd_back(t_stack **lst, t_stack *new)
{
	t_stack	*current;

	current = *lst;
	if (!lst || !new)
		return ;
	if (*lst == NULL)
	{
		*lst = new;
		return ;
	}
	while (current->next)
		current = current->next;
	current->next = new;
	new->next = NULL;
}
