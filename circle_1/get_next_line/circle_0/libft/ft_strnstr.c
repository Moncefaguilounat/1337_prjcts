/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 11:00:11 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/16 18:28:59 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <bsd/string.h>
#include "libft.h"

char	*ft_strnstr(const char *big, const char *little, size_t n)
{
	size_t	i;
	size_t	j;
	size_t	k;

	i = 0;
	if (!little[0])
		return ((char *)big);
	while (big[i] && i < n)
	{
		j = 0;
		k = i;
		while (k < n && big[k] && little[j] && big[k] == little[j])
		{
			k++;
			j++;
		}
		if (little[j] == '\0')
			return ((char *)&big[i]);
		i++;
	}
	return (NULL);
}
/*
int	main()
{
	char s1[] = "Boo Bar Baz";
	char s2[] = "bar";

	printf("myf :%s    ", ft_strnstr(s1, s2, 9));
        printf("sdf :%s\n", strnstr(s1, s2, 9));
}*/
