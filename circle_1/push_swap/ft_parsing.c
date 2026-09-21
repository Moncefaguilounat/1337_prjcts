/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_parsing.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 13:58:43 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 13:58:45 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

static void	ft_parsing_error(char **tmp, t_stack **a)
{
	ft_freestr(tmp);
	ft_lstclear(a);
	ft_error();
}

t_stack	*ft_parsing(int ac, char **av)
{
	t_stack	*a;
	char	**tmp;

	int (i), j, n, flag;
	a = NULL;
	i = 1;
	while (i < ac)
	{
		j = 0;
		tmp = ft_split(av[i++]);
		while (tmp[j])
		{
			n = ft_validate_str(tmp[j++], &flag);
			if (!flag || !ft_checkdup(a, n))
				ft_parsing_error(tmp, &a);
			else
				ft_lst_stack(&a, n);
		}
		ft_freestr(tmp);
	}
	return (a);
}
