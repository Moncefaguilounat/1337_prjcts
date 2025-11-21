/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 14:17:46 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/23 09:39:11 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_calloc(size_t nmemb, size_t size)
{
	char	*p;
	size_t	i;
	size_t	bytes;

	i = 0;
	if (size == 0 || nmemb == 0)
		return (malloc(0));
	if (nmemb > SIZE_MAX / size)
		return (NULL);
	bytes = (nmemb * size);
	p = malloc(bytes);
	if (!p)
		return (NULL);
	while (i < bytes)
		p[i++] = 0;
	return ((void *)p);
}
/*
int	main()
{
	char *str = (char *)calloc(SIZE_MAX, 2);

	*str = 5;
}*/
