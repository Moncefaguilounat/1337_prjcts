/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 11:27:35 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/21 19:06:35 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

// D < s ka nbdaw ncopiew mn loor
void	*ft_memmove(void *dest, const void *src, size_t n)
{
	const unsigned char	*s;
	unsigned char		*d;

	d = dest;
	s = src;
	if (d == s || n == 0)
		return (dest);
	if (d < s)
	{
		while (n--)
			*d++ = *s++;
	}
	else
	{
		d += n;
		s += n;
		while (n--)
			*--d = *--s;
	}
	return (dest);
}
/*
int	main()
{
	char str[] = "aguilounat";
	printf("sdf :%s   \n", (char *)memmove(str, str , 4));
	printf("myf :%s", (char *)ft_memmove(str, str, 4));
}*/
