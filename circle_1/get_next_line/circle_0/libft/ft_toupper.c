/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_toupper.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 18:14:52 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/16 18:15:43 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <ctype.h>
#include "libft.h"

int	ft_toupper(int c)
{
	if (c >= 97 && c <= 122)
		c = c - 32;
	return (c);
}

/*int	main()
{
	char str[] = "abcEFJ!@12:	\n";
	int i = 0;
	while(str[i])
	{
		printf("myf :%d  , ", ft_toupper(str[i]));
		printf("sdf : %d\n", toupper(str[i]));
		i++;
	}
}*/
