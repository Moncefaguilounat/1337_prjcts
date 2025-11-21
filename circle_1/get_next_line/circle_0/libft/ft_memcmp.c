/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/19 09:32:25 by mouaguil          #+#    #+#             */
/*   Updated: 2025/10/19 09:47:12 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <string.h>
#include "libft.h"

int	ft_memcmp(const void *s1, const void *s2, size_t n)
{
	const unsigned char	*str1;
	const unsigned char	*str2;

	str1 = s1;
	str2 = s2;
	while (n--)
	{
		if (*str1 != *str2)
			return (*str1 - *str2);
		str1++;
		str2++;
	}
	return (0);
}

/*int main(void)
{
    char a1[] = "hello";
    char a2[] = "hello";
    char b1[] = "hello";
    char b2[] = "hezlo"; // diff in the 3rd byte
    char c1[] = "abcd";
    char c2[] = "abCd";  // diff in 3rd byte (case)
    char d1[] = "abc\0def";
    char d2[] = "abc\0xyz";
    unsigned char e1[] = {255, 0, 127};
    unsigned char e2[] = {0, 0, 127};

    printf("%d | %d\n", memcmp(a1, a2, 5), ft_memcmp(a1, a2, 5));
    printf("%d | %d\n", memcmp(b1, b2, 5), ft_memcmp(b1, b2, 5));
    printf("%d | %d\n", memcmp(c1, c2, 4), ft_memcmp(c1, c2, 4));
    printf("%d | %d\n", memcmp(c1, c2, 2), ft_memcmp(c1, c2, 2));
    printf("%d | %d\n", memcmp(d1, d2, 7), ft_memcmp(d1, d2, 7));
    printf("%d | %d\n", memcmp(e1, e2, 3), ft_memcmp(e1, e2, 3));
    printf("%d | %d\n", memcmp(a1, a2, 0), ft_memcmp(a1, a2, 0));

    return 0;
}*/
