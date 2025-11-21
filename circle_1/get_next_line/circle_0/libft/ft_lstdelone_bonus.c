/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstdelone_bonus.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 10:07:39 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/29 13:56:37 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*void	del(void *content)
{
	if (content == NULL)
		return ;
	free(content);
}*/
void	ft_lstdelone(t_list *lst, void (*del)(void *))
{
	if (!lst)
		return ;
	if (!del)
		return ;
	del(lst->content);
	free(lst);
}
/*
int main(void)
{
    t_list *node = malloc(sizeof(t_list));
    if (!node)
        return (1);
    node->content = malloc(20);
    if (!node->content)
    {
        free(node);
        return (1);
    }
    sprintf((char *)node->content, "Hello, world!");
    node->next = NULL;

    ft_lstdelone(node, del);

    return (0);
}
*/
