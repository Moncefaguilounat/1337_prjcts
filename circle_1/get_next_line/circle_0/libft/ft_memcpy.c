/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 10:33:51 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/28 18:12:27 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	const unsigned char	*s;
	unsigned char		*d;

	if (dest == src)
		return (dest);
	d = (unsigned char *)dest;
	s = (const unsigned char *)src;
	while (n--)
		*d++ = *s++;
	return (dest);
}
/*
int	main()
{
	char src[] = "Moncef";
//	char dest[50];
	ft_memcpy(src + 2,src, 7);
//	printf("%s\n", dest);
//	ft_memcpy(dest, src, 7);
	printf("%s", src);
}*/
