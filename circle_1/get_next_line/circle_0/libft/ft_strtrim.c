/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 15:02:05 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/22 15:02:07 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	front_trim(char const *s1, char const *set)
{
	int	f;

	f = 0;
	while (s1[f] && ft_strchr(set, s1[f]))
		f++;
	return (f);
}

static int	back_trim(const char *s1, char const *set)
{
	int	b;

	b = 0;
	while (s1[b])
		b++;
	b--;
	while (b >= 0 && ft_strchr(set, s1[b]))
		b--;
	return (b);
}

char	*ft_strtrim(char const *s1, char const *set)
{
	int		f;
	int		b;

	if (!s1)
		return (NULL);
	if (!set)
		return (ft_strdup(s1));
	if (set[0] == '\0')
		return (ft_strdup(s1));
	f = front_trim(s1, set);
	if (s1[f] == '\0')
		return (ft_strdup(""));
	b = back_trim(s1, set);
	return (ft_substr(s1, f, b - (f - 1)));
}
/*
int	main()
{
	char str[] = "aabaa";
	char *to_trim = "";
	char *res = ft_strtrim(str, to_trim);
	if(*res == '\0')
		printf("byte terminator");
	else
	printf("%s", res);
	free(res);
}*/
