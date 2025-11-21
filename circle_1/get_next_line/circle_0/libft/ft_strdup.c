/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 12:41:28 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/21 14:57:01 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strdup(const char *s)
{
	int		i;
	char	*str;

	i = 0;
	while (s[i])
		i++;
	str = malloc(i + 1);
	if (!str)
		return (NULL);
	i = 0;
	while (s[i])
	{
		str[i] = s[i];
		i++;
	}
	str[i] = '\0';
	return (str);
}
/*
int	main()
{
	char str[] = "";
	char *res_myf = ft_strdup(str);
	char *res_sdf = strdup(str);
	printf("myf :%s    ", res_myf);
	printf("sdf :%s\n", res_sdf);
	free(res_myf);
	free(res_sdf);
}
*/
