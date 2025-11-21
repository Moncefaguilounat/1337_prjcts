/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 18:32:24 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/21 19:20:32 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <string.h>
#include "libft.h"

char	*ft_strchr(const char *s, int c)
{
	int	i;

	i = 0;
	if ((char)c == '\0')
	{
		while (*s)
			s++;
		return ((char *)s);
	}
	while (s[i])
	{
		if (s[i] == (char)c)
			return ((char *)&s[i]);
		i++;
	}
	return (NULL);
}
/*
int	main()
{
	char str[]  = "abcdefjh12@";

	printf("myf :%s    ", ft_strchr(str, '\0'));
	printf("sdf :%s\n", strchr(str, '\0'));
}*/
