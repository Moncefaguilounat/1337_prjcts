/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_checker_utils.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/11 15:09:00 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/11 15:09:02 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

//functions that helps the checker
void	ok_ko(int f)
{
	if (f)
		write (1, "OK\n", 3);
	else
		write (1, "KO\n", 3);
}

int	final_check(t_stack *a, t_stack *b)
{
	if (!ft_checksorted(a))
		return (0);
	if (b != NULL)
		return (0);
	return (1);
}

void	apply_instr(char *instr, t_stack **a, t_stack **b)
{
	if (!ft_strcmp("sa\n", instr))
		ft_sa(a, 0);
	else if (!ft_strcmp("sb\n", instr))
		ft_sb(b, 0);
	else if (!ft_strcmp("ss\n", instr))
		ft_ss(a, b, 0);
	else if (!ft_strcmp("pa\n", instr))
		ft_pa(a, b, 0);
	else if (!ft_strcmp("pb\n", instr))
		ft_pb(a, b, 0);
	else if (!ft_strcmp("ra\n", instr))
		ft_ra(a, 0);
	else if (!ft_strcmp("rb\n", instr))
		ft_rb(b, 0);
	else if (!ft_strcmp("rr\n", instr))
		ft_rr(a, b, 0);
	else if (!ft_strcmp("rra\n", instr))
		ft_rra(a, 0);
	else if (!ft_strcmp("rrb\n", instr))
		ft_rrb(b, 0);
	else if (!ft_strcmp("rrr\n", instr))
		ft_rrr(a, b, 0);
}

void	clear_and_error(char *instr, t_stack **a, t_stack **b)
{
	free(instr);
	ft_lstclear(a);
	if (b)
		ft_lstclear(b);
	ft_error();
}

int	validate_instruction(char *instruction)
{
	if (!ft_strcmp("sa\n", instruction))
		return (1);
	else if (!ft_strcmp("sb\n", instruction))
		return (1);
	else if (!ft_strcmp("ss\n", instruction))
		return (1);
	else if (!ft_strcmp("pa\n", instruction))
		return (1);
	else if (!ft_strcmp("pb\n", instruction))
		return (1);
	else if (!ft_strcmp("ra\n", instruction))
		return (1);
	else if (!ft_strcmp("rb\n", instruction))
		return (1);
	else if (!ft_strcmp("rr\n", instruction))
		return (1);
	else if (!ft_strcmp("rra\n", instruction))
		return (1);
	else if (!ft_strcmp("rrb\n", instruction))
		return (1);
	else if (!ft_strcmp("rrr\n", instruction))
		return (1);
	return (0);
}
