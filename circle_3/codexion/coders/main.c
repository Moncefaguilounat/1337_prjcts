#include "parse.h"
#include "init.h"
#include "simulation.h"
#include "cleanup.h"

int main(int argc, char **argv)
{
    t_simulation    sim;

    if (parse_arguments(argc, argv, &sim) == FAILURE)
    {
        printf("Error: invalid arguments\n");
        return (FAILURE);
    }
    if (init_simulation(&sim) == FAILURE)
    {
        printf("Error: initialization failed\n");
        return (FAILURE);
    }
    if (run_simulation(&sim) == FAILURE)
    {
        cleanup_simulation(&sim, sim.number_of_coders);
        printf("Error: simulation failed\n");
        return (FAILURE);
    }
    cleanup_simulation(&sim, sim.number_of_coders);
    return (SUCCESS);
}
