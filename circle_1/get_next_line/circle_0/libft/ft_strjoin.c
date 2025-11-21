/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/19 11:37:01 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/25 12:29:05 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <stdlib.h>
//#include <string.h>
#include "libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*res;
	size_t	s_lens;
	size_t	i;

	if (!s1 || !s2)
		return (NULL);
	s_lens = ft_strlen(s1) + ft_strlen(s2);
	res = malloc(s_lens + 1);
	if (!res)
		return (NULL);
	i = 0;
	while (*s1)
		res[i++] = *s1++;
	while (*s2)
		res[i++] = *s2++;
	res[i] = '\0';
	return (res);
}
/*
int	main()
{
	//char str1[] = "hyd fihalatk";
	//char str2[] = " akha ysenhaji";
	char *str1 = NULL;
	char *str2 = NULL;

	char *res = ft_strjoin(str1, str2);
	printf("%s", res);
	free(res);
}*/
