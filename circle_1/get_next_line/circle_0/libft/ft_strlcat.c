/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 16:11:57 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/30 14:42:46 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	dlen;
	size_t	slen;
	size_t	i;

	dlen = 0;
	slen = 0;
	i = 0;
	if (size == 0)
		return (ft_strlen(src));
	while (src[slen])
		slen++;
	while (dlen < size && dst[dlen])
		dlen++;
	if (size <= dlen)
		return (slen + size);
	while ((dlen + i + 1) < size && src[i] != '\0')
	{
		dst[dlen + i] = src[i];
		i++;
	}
	dst[dlen + i] = '\0';
	return (dlen + slen);
}
/*
int	main()
{
	char s[12];
	char d[12];
	strlcat(d, s, 12);
	printf("%s\n" , d);
	ft_strlcat(d, s, 12);
	printf("%s", d);
	return 0;
}*/
