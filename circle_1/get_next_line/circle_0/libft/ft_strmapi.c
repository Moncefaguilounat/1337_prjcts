/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/20 11:54:46 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/20 15:55:32 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*char	test(unsigned int i, char c)
{
	i = i + 1;
	printf("%d", i);
	c = c + 1;
	return (c);
}
*/
char	*ft_strmapi(char const *s, char (*f)(unsigned int, char))
{
	unsigned int	i;
	char			*res;

	i = 0;
	if (!s || !f)
		return (NULL);
	i = ft_strlen(s);
	res = malloc(i + 1);
	if (!res)
		return (NULL);
	res[i] = '\0';
	i = 0;
	while (s[i])
	{
		res[i] = f(i, s[i]);
		i++;
	}
	return (res);
}
/*
int	main()
{
	const char *str = "";
	char *res = ft_strmapi(str, test);
	printf ("%s\n", res);
}*/
