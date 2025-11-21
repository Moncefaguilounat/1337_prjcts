/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/19 09:58:03 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/29 15:50:51 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char			*res;
	unsigned int	i;

	if (!s)
		return (NULL);
	i = ft_strlen(s);
	if (i <= start || len == 0)
	{
		res = malloc(1);
		if (!res)
			return (NULL);
		*res = '\0';
		return (res);
	}
	if (start + len > (size_t)i)
		len = i - start;
	res = malloc(len + 1);
	if (!res)
		return (NULL);
	i = 0;
	while (len--)
		res[i++] = s[start++];
	res[i] = '\0';
	return (res);
}
