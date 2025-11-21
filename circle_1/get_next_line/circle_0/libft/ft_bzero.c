/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 09:55:30 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/16 18:06:31 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <string.h>
#include "libft.h"

void	ft_bzero(void *s, size_t n)
{
	unsigned char	*str;

	str = (unsigned char *)s;
	while (n--)
		*str++ = 0;
}

/*int	main()
{
	char str[] = "ana smiti moncef";
	bzero(str + 4, 5);
	int i = 0;
	while(i < 16)
		printf("%d ,", str[i++]);
	printf("\n");
	ft_bzero(str + 4, 5);
	i = 0;
	while(i < 16)
		printf("%d ,", str[i++]);
	printf("\n");
}*/
