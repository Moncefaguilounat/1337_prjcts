/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstiter.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 13:41:28 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/24 14:06:47 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
/*
void	f(void *content)
{
	printf("%s\n", (char *)content);
}*/
void	ft_lstiter(t_list *lst, void (*f)(void *))
{
	t_list	*iter;

	if (!lst || !f)
		return ;
	iter = lst;
	while (iter)
	{
		f(iter->content);
		iter = iter->next;
	}
}
/*
int	main()
{
	t_list *head = ft_lstnew("Hello");
	t_list *n2 = ft_lstnew("ana");
	t_list *n3 = ft_lstnew("moncef");
	head->next = n2;
	n2->next = n3;
	n3->next = NULL;
	ft_lstiter(head, f);
	free(head);
	free(n2);
	free(n3);
}*/
