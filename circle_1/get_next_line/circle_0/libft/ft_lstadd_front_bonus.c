/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_front.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/23 11:03:06 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/23 14:39:08 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstadd_front(t_list **lst, t_list *new)
{
	if (!lst || !new)
		return ;
	new->next = *lst;
	*lst = new;
}
/*
int	main()
{
	t_list *head = NULL;
	t_list *world = ft_lstnew("world");
	t_list *hello = ft_lstnew("hello");
	ft_lstadd_front(&head, world);
	ft_lstadd_front(&head, hello);

	t_list *index = head;
	while (index)
	{
		printf("%s ", (char *)index->content);
		index = index->next;
	}
}*/	
