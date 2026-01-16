/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 15:17:26 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/08 15:17:33 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "push_swap.h"

static int	ft_nb_of_words(char const *s)
{
	int	i;
	int	count;
	int	in_word;

	i = 0;
	count = 0;
	in_word = 0;
	while (s[i])
	{
		if (s[i] != ' ' && !in_word)
		{
			in_word = 1;
			count++;
		}
		else if (s[i] == ' ')
			in_word = 0;
		i++;
	}
	return (count);
}

static int	ft_fill_word(char const *s, int i, char **result, int x)
{
	int	j;

	j = 0;
	while (s[i + j] && s[i + j] != ' ')
		j++;
	result[x] = malloc(j + 1);
	if (!result[x])
		return (-1);
	j = 0;
	while (s[i] && s[i] != ' ')
	{
		result[x][j] = s[i];
		i++;
		j++;
	}
	result[x][j] = '\0';
	return (i);
}

char	**ft_split(char const *s)
{
	int		i;
	int		x;
	char	**result;

	if (!s)
		return (NULL);
	result = malloc(sizeof(char *) * (ft_nb_of_words(s) + 1));
	if (!result)
		return (NULL);
	i = 0;
	x = 0;
	while (s[i])
	{
		while (s[i] && s[i] == ' ')
			i++;
		if (s[i])
		{
			i = ft_fill_word(s, i, result, x);
			if (i == -1)
				return (ft_freestr(result), NULL);
			x++;
		}
	}
	return (result[x] = NULL, result);
}
