/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_back_bonus.c                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 09:35:24 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/30 16:10:06 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstadd_back(t_list **lst, t_list *new)
{
	t_list	*current;

	if (!lst || !new)
		return ;
	current = *lst;
	if (*lst == NULL)
	{
		*lst = new;
		return ;
	}
	while (current->next)
		current = current->next;
	current->next = new;
}
/*
int main(void)
{
    t_list *list = NULL;
    t_list *n1 = ft_lstnew("one");
    t_list *n2 = ft_lstnew("two");
    t_list *n3 = ft_lstnew("three");

    ft_lstadd_back(&list, n1);
    ft_lstadd_back(&list, n2);
    ft_lstadd_back(&list, n3);

    t_list *printt;
    printt = list;
    while (printt)
    {    
	    printf("%s\n", (char *)printt->content);
		printt = printt->next;
    }
    free(n1);
    free(n2);
    free(n3);

    return (0);
}*/
