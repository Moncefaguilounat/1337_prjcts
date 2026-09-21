/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lst_utils2.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 13:58:08 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 13:58:10 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

//this functions frees the tmp we use in the parsing
void	ft_freestr(char **lst)
{
	char	*n1;
	char	**str;

	if (!lst)
		return ;
	str = lst;
	while (*lst)
	{
		n1 = *lst;
		lst++;
		free(n1);
	}
	free(str);
}

//this function is supposed to create the stack 
//after the arguments are validated 
//we add them using lstaddback and 
//ft_lstnew 
void	ft_lst_stack(t_stack **a, int n)
{
	ft_lstadd_back(a, ft_lstnew(&n));
}

// this function returns the index of 
// the max element in the stack
int	ft_max_index(t_stack *s)
{
	int	max;

	max = s->index;
	while (s)
	{
		if (s->index > max)
			max = s->index;
		s = s->next;
	}
	return (max);
}

// this function returns the index of 
// the min element in the stack
int	ft_min_index(t_stack *s)
{
	int	min;

	min = s->index;
	while (s)
	{
		if (s->index < min)
			min = s->index;
		s = s->next;
	}
	return (min);
}

//this functions returns the position of
//an element in the stack
int	ft_find_position(t_stack *s, int index)
{
	int	pos;

	pos = 0;
	while (s)
	{
		if (s->index == index)
			return (pos);
		pos++;
		s = s->next;
	}
	return (-1);
}
