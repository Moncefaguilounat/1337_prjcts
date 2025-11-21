/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putendl_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 11:40:34 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/22 11:40:48 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putendl_fd(char *s, int fd)
{
	if (!s)
		return ;
	write (fd, s, ft_strlen(s));
	write (fd, "\n", 1);
}
/*
int     main()
{
        int fd = open("test.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
	if ( fd == -1)
		printf ("something went wrong");
        ft_putendl_fd("anas", fd);
	close(fd);
}*/
