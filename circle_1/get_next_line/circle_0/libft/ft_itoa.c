/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/19 18:24:58 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/22 10:37:41 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	digits_count(long n)
{
	int	count;

	count = 0;
	if (n <= 0)
		count = 1;
	while (n != 0)
	{
		n /= 10;
		count++;
	}
	return (count);
}

char	*ft_itoa(int n)
{
	char	*res;
	int		len;
	long	t;

	t = n;
	len = digits_count(t);
	res = malloc(len + 1);
	if (!res)
		return (NULL);
	res[len] = '\0';
	if (t < 0)
	{
		res[0] = '-';
		t = -t;
	}
	if (t == 0)
		res[0] = '0';
	while (t > 0)
	{
		res[--len] = (t % 10) + '0';
		t = t / 10;
	}
	return (res);
}
/*
int	main()
{
	char *s = ft_itoa(0);
	printf ("%s", s);
}*/
