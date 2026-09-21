# include "parse.h"

int     is_positive_number(char *str)
{
    int i;

    i = 0;
    if (!str[i])
        return (FAILURE);

    while (str[i])
    {
        if (str[i] < '0' || str[i] > '9')
            return (FAILURE);
        i++;
    }
    return (SUCCESS);
}

int     ft_atol(char *str, long *result)
{
    int     digit;

    *result = 0;
    while (*str)
    {
        digit = *str - '0';
        if (*result > (LONG_MAX - digit) / 10)
            return (FAILURE);
        *result = *result * 10 + digit;
        str++;
    }
    return (SUCCESS);
}

int     valid_scheduler(char *str)
{
    if (strcmp(str, "fifo") == 0)
        return (SUCCESS);
    if (strcmp(str, "edf") == 0)
        return (SUCCESS);
    return (FAILURE);
}
