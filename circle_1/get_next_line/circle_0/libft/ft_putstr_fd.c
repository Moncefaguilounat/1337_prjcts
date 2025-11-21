/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 15:01:14 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/22 15:01:17 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putstr_fd(char *s, int fd)
{
	if (!s)
		return ;
	write (fd, s, ft_strlen(s));
}
/*
int     main()
{
        int fd = open("test.txt", O_CREAT | O_WRONLY, 0644);
	if (fd == -1)
		printf ("something went wrong");
        ft_putstr_fd("anas", fd);
	close(fd);
}*/
