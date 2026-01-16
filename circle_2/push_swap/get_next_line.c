/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/10 16:08:51 by mouaguil          #+#    #+#             */
/*   Updated: 2025/11/10 16:08:53 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static char	*read_append(int fd, char *saved, int *flag)
{
	char	*tmp;
	int		rd;
	char	*new_saved;

	tmp = malloc(BUFFER_SIZE + 1);
	if (!tmp)
		return (free(saved), NULL);
	rd = read(fd, tmp, BUFFER_SIZE);
	if (rd < 0)
		return (free(tmp), free(saved), NULL);
	if (rd == 0)
	{
		free(tmp);
		return (*flag = 1, saved);
	}
	tmp[rd] = '\0';
	if (!saved)
	{
		new_saved = ft_strdup(tmp);
		free(tmp);
		return (new_saved);
	}
	new_saved = ft_strjoin(saved, tmp);
	return (free(tmp), free(saved), new_saved);
}

static char	*extract_line(char *saved)
{
	int	i;

	if (!saved || !saved[0])
		return (NULL);
	i = 0;
	while (saved[i] && saved[i] != '\n')
	{
		i++;
	}
	if (saved[i] == '\n')
	{
		i++;
	}
	return (ft_substr(saved, 0, i));
}

static char	*update_saved(char *saved)
{
	char	*new_saved;
	int		i;

	if (!saved)
		return (NULL);
	i = 0;
	while (saved[i] && saved[i] != '\n')
		i++;
	if (saved[i] == '\n')
		i++;
	if (!saved[i])
	{
		free (saved);
		return (NULL);
	}
	new_saved = ft_substr(saved, i, ft_strlen(saved) - i);
	free(saved);
	return (new_saved);
}

char	*get_next_line(int fd)
{
	static char	*saved;
	char		*line;
	int			flag;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	flag = 0;
	saved = read_append(fd, saved, &flag);
	while ((!saved || !ft_strchr(saved, '\n')) && !flag)
	{
		saved = read_append(fd, saved, &flag);
		if (!saved)
			return (NULL);
	}
	line = extract_line(saved);
	saved = update_saved(saved);
	return (line);
}
