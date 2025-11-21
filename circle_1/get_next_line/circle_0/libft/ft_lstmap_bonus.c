/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap_bonus.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 14:50:28 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/30 16:06:05 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	void	*content;

	t_list *(head), *(new);
	if (!lst || !f || !del)
		return (NULL);
	head = NULL;
	while (lst)
	{
		content = f(lst->content);
		if (!content)
		{
			ft_lstclear(&head, del);
			return (NULL);
		}
		new = ft_lstnew(content);
		if (!new)
		{
			del(content);
			ft_lstclear(&head, del);
			return (NULL);
		}
		ft_lstadd_back(&head, new);
		lst = lst->next;
	}
	return (head);
}
/*
#include <stdio.h>
void *add_one(void *content)
{
    int *new = malloc(sizeof(int));
    *new = (*(int *)content) + 1;
    return (new);
}

void del(void *content)
{
    free(content);
}

int main(void)
{
    t_list *list;
    t_list *result;
    int *a = malloc(sizeof(int));
    int *b = malloc(sizeof(int));

    *a = 5;
    *b = 10;

    list = ft_lstnew(a);
    list->next = ft_lstnew(b);

    result = ft_lstmap(list, add_one, del);

    printf("%d\n", *(int *)result->content);
    printf("%d\n", *(int *)result->next->content);

    ft_lstclear(&list, del);
    ft_lstclear(&result, del);

    return (0);
}*/
