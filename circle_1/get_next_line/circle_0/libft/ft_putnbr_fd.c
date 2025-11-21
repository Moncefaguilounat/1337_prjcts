/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 11:58:29 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/21 14:01:38 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putnbr_fd(int n, int fd)
{
	char	c;
	long	num;

	num = n;
	if (num < 0)
	{
		write(fd, "-", 1);
		num = -num;
	}
	if (num / 10)
		ft_putnbr_fd(num / 10, fd);
	c = num % 10 + '0';
	write (fd, &c, 1);
}
/*
int	main()
{
	int fd = open("test.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
	if (fd == -1)
	
		printf("something went wrong");
		return 1;
	}
	int n = 0;

	ft_putnbr_fd(n , fd);
	close(fd);
}*/	
