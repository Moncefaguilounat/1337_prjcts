/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstclear_bonus.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 11:15:28 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/29 14:00:32 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*void  del(void *content)
{
        if (content == NULL)
                return ;
        free(content);
}
*/
void	ft_lstclear(t_list **lst, void (*del)(void*))
{
	t_list	*current;
	t_list	*d;

	if (!lst || !*lst || !del)
		return ;
	current = *lst;
	while (current)
	{
		del(current->content);
		d = current;
		current = current->next;
		free(d);
	}
	*lst = NULL;
}
/*
int main(void)
{
    t_list *head;
    t_list *node2;
    t_list *node3;

    head = malloc(sizeof(t_list));
    node2 = malloc(sizeof(t_list));
    node3 = malloc(sizeof(t_list));
    if (!head || !node2 || !node3)
        return 1;

    head->content = malloc(20);
    node2->content = malloc(20);
    node3->content = malloc(20);
    if (!head->content || !node2->content || !node3->content)
        return 1;

    sprintf((char *)head->content, "Node 1");
    sprintf((char *)node2->content, "Node 2");
    sprintf((char *)node3->content, "Node 3");

    head->next = node2;
    node2->next = node3;
    node3->next = NULL;

    ft_lstclear(&head, del);
    if (!head)
        printf("List successfully cleared.\n");
    else
        printf("Error: list not cleared.\n");

    return 0;
}*/
