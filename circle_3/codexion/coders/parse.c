#include "parse.h"

static int  check_argc(int ac)
{
    if (ac != 9)
        return (FAILURE);
    return (SUCCESS);
}

static int  validate_arguments(char **av)
{
    int     i;
    long    value;

    i = 1;
    while (i < 8)
    {
        if (is_positive_number(av[i]) == FAILURE)
            return (FAILURE);
        if (ft_atol(av[i], &value) == FAILURE)
            return (FAILURE);
        if ((i == 1 || i == 6) && value <= 0)
            return (FAILURE);
        if (value < 0 || value > INT_MAX)
            return (FAILURE);
        i++;
    }
    if (valid_scheduler(av[8]) == FAILURE)
        return (FAILURE);
    return (SUCCESS);
}

static void fill_simulation(t_simulation *sim, char **argv)
{
    long    values[7];
    int     i;

    i = 0;
    while (i < 7)
    {
        ft_atol(argv[i + 1], &values[i]);
        i++;
    }
    sim->number_of_coders = (int)values[0];
    sim->time_to_burnout = values[1];
    sim->time_to_compile = values[2];
    sim->time_to_debug = values[3];
    sim->time_to_refactor = values[4];
    sim->max_compiles = (int)values[5];
    sim->dongle_cooldown = values[6];
    if (strcmp(argv[8], "fifo") == 0)
        sim->scheduler = FIFO;
    else
        sim->scheduler = EDF;
}

int parse_arguments(int argc, char **argv, t_simulation *sim)
{
    if (check_argc(argc) == FAILURE)
        return (FAILURE);
    if (validate_arguments(argv) == FAILURE)
        return (FAILURE);
    fill_simulation(sim, argv);
    return (SUCCESS);
}
