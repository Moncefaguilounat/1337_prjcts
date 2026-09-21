/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_validate_str.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 16:04:06 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 16:04:07 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

static int	ft_validate_str_sub(const char *str, int *flag, int mod)
{
	long long	i;

	i = 0;
	while (*str)
	{
		if (!ft_isdigit(*str))
			return (*flag = 0, 0);
		i = i * 10 + (*str - 48);
		str++;
	}
	if ((mod * i) > 2147483647 || (mod * i) < -2147483648)
		return (*flag = 0, 0);
	return (mod * i);
}

int	ft_validate_str(const char *str, int *flag)
{
	int	indx;
	int	mod;

	mod = 1;
	*flag = 1;
	indx = 0;
	while (str[indx] == ' ')
		indx++;
	if (str[indx] == '-')
	{
		mod = -1;
		indx++;
	}
	else if (str[indx] == '+')
		indx++;
	if (!ft_isdigit(str[indx]))
		return (*flag = 0, 0);
	return (ft_validate_str_sub(str + indx, flag, mod));
}
