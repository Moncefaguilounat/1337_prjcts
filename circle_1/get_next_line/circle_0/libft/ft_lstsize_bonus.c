/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstsize_bonus.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 09:46:21 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/29 13:53:52 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_lstsize(t_list *lst)
{
	int	i;

	i = 0;
	if (!lst)
		return (0);
	while (lst)
	{
		lst = lst->next;
		i++;
	}
	return (i);
}
/*
#include <stdio.h>
int	main()
{
	//t_list *n1 = ft_lstnew("Hello");
	//t_list *n2 = ft_lstnew("i am");
	//t_list *n3 = ft_lstnew("moncef");

	//n1->next = n2;
	//n2->next = n3;
	//n3->next = NULL;
	int size = ft_lstsize(NULL);
	printf ("%d\n", size);
//	free(n1);
//	free(n2);
//	free(n3);
}
*/
