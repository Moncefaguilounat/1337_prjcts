/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstlast.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 09:59:11 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/24 14:08:19 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstlast(t_list *lst)
{
	if (!lst)
		return (NULL);
	while (lst->next)
		lst = lst->next;
	return (lst);
}
/*
int	main()
{
        //t_list *n1 = ft_lstnew("Hello");
        //t_list *n2 = ft_lstnew("i am");
        //t_list *n3 = ft_lstnew("moncef");

        //n1->next = n2;
        //n2->next = n3;
        //n3->next = NULL;
        t_list *res = ft_lstlast(NULL);
	if (!res)
	{
		printf("Da Null");
		return 0;
	}
        printf ("%s\n", (char *)res->content);
//	free(n1);
//	free(n2);
//	free(n3);
}*/
