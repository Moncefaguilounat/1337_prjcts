/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_checker.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/11 14:45:23 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/11 14:45:24 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

void	ft_checker(int ac, char **av)
{
	t_stack	*a;
	t_stack	*b;
	char	*instr;

	b = NULL;
	a = ft_parsing(ac, av);
	instr = get_next_line(0);
	if (!instr)
	{
		ok_ko(final_check(a, b));
		ft_lstclear(&a);
		return ;
	}
	while (instr)
	{
		if (!validate_instruction(instr))
			clear_and_error(instr, &a, &b);
		apply_instr(instr, &a, &b);
		free(instr);
		instr = get_next_line(0);
	}
	ok_ko(final_check(a, b));
	ft_lstclear(&a);
}

int	main(int ac, char **av)
{
	int	i;

	i = 0;
	if (ac < 2)
		return (0);
	while (i < ac)
	{
		if (!ft_just_spaces(av[i]))
			ft_error();
		i++;
	}
	ft_checker(ac, av);
	return (0);
}
