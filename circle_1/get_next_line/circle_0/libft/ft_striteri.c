/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_striteri.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/20 14:32:40 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/20 18:22:46 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*void  test(unsigned int i, char *c)
{
        i = i + 1;
        printf("%d   ", i);
        *c = *c + 1;
	printf("%c \n", *c);
}
*/
void	ft_striteri(char *s, void (*f)(unsigned int, char*))
{
	unsigned int	i;

	i = 0;
	while (s[i])
	{
		f(i, (s + i));
		i++;
	}
}
/*
int     main()
{
        char str[] = "abc";
        ft_striteri(str, test);
}
*/
