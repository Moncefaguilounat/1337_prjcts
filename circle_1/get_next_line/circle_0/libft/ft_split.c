/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 14:58:34 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/24 18:10:11 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_nb_of_words(char const *s, char c)
{
	int	i;
	int	count;
	int	in_word;

	i = 0;
	count = 0;
	in_word = 0;
	while (s[i])
	{
		if (s[i] != c && !in_word)
		{
			in_word = 1;
			count++;
		}
		else if (s[i] == c)
			in_word = 0;
		i++;
	}
	return (count);
}

static char	*ft_fill_word(char const *s, int *i, char c)
{
	int		j;
	int		y;
	char	*result;

	j = 0;
	y = *i;
	while (s[y + j] && s[y + j] != c)
		j++;
	result = malloc(j + 1);
	if (!result)
		return (NULL);
	j = 0;
	while (s[y] && s[y] != c)
	{
		result[j] = s[y];
		y++;
		j++;
	}
	result[j] = '\0';
	*i = y;
	return (result);
}

static void	*freeing(char **result, int x)
{
	while (x >= 0)
		free(result[x--]);
	free(result);
	return (NULL);
}

char	**ft_split(char const *s, char c)
{
	char	**result;

	int i, (x);
	if (!s)
		return (NULL);
	result = malloc(sizeof(char *) * (ft_nb_of_words(s, c) + 1));
	if (!result)
		return (NULL);
	i = 0;
	x = 0;
	while (s[i])
	{
		while (s[i] && s[i] == c)
			i++;
		if (s[i])
		{
			result[x] = ft_fill_word(s, &i, c);
			if (!result[x])
				return (freeing(result, x));
			x++;
		}
	}
	result[x] = NULL;
	return (result);
}
/*
int     main()
{
    char **tab = ft_split(NULL, '+');
    //char **tab = ft_split("", '+');
    //char **tab = ft_split("hello", 'x');
    //char **tab = ft_split(",,,", ',');
    //char **tab = ft_split(",a,,b,", ',');
    int i = 0;
    if (!tab)
    {
        printf("da NULL");
        return 0;
    }
    while (tab[i])
    {
        printf("%s ", tab[i]);
        free(tab[i]);
        i++;
    }
    printf("\n");
    free(tab);
    return 0;
}*/
