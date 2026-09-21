#ifndef PARSE_H
# define PARSE_H

# include "types.h"
# include <limits.h>

int     parse_arguments(int argc, char **argv, t_simulation *sim);

int     is_positive_number(char *str);
int     ft_atol(char *str, long *value);
int     valid_scheduler(char *scheduler);

#endif
