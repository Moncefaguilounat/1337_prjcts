/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/13 18:52:23 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/30 12:48:12 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *s, int c, size_t n)
{
	unsigned char	*str;
	unsigned char	val;

	val = (unsigned char)c;
	str = (unsigned char *)s;
	while (n--)
		*str++ = val;
	return (s);
}
/*
#include <stdio.h>

int	main()
{
	//char str[] = "ana ***** Moncef";
	int r = 0;
		ft_memset((char *)&r, 0b11000111, 1);
		ft_memset((char *)&r + 1, 0b11111010, 1);
		//ft_memset((char *)&r + 2, 0b00000000, 1);
		//ft_memset((char *)&r + 3, 0b00000000, 1);


		//ft_memset((unsigned char *)&r + 1, 0b11111111, 1);
		ft_memset((char *)&r + 2, 0b11111111, 1);
		ft_memset((char *)&r + 3, 0b11111111, 1);
	printf("%d", r);
}
*/
/*
#include <stdio.h>
int main()
{
	int   a = -12345;
	int b = 0 ;
	int i = 0;
	while(i <= 3)
	{
		char c = a >> (8*i);
		ft_memset( (unsigned char *)&b + i ,c , 1);
		i++;
	}
	printf("%d" , b);
}*/
