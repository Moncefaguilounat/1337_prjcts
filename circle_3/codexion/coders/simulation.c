#include "simulation.h"

static void initialize_simulation(t_simulation *sim)
{
    int i;

    i = 0;
    sim->start_time = get_time_ms(sim);
    while (i < sim->number_of_coders)
    {
        sim->coders[i].last_compile_time = sim->start_time;
        i++;
    }
}

static int  create_monitor_thread(t_simulation *sim)
{
    if (pthread_create(&sim->monitor_thread,
        NULL, monitor_routine, sim) != 0)
        return (FAILURE);
    return (SUCCESS);
}

static int  join_monitor_thread(t_simulation *sim)
{
    if (pthread_join(sim->monitor_thread, NULL) != 0)
        return (FAILURE);
    return (SUCCESS);
}

int run_simulation(t_simulation *sim)
{
    initialize_simulation(sim);
    if (create_coder_threads(sim) == FAILURE)
        return (FAILURE);
    initialize_simulation(sim);
    if (create_monitor_thread(sim) == FAILURE)
    {
        stop_simulation(sim);
        join_coder_threads(sim);
        return (FAILURE);
    }
    if (join_monitor_thread(sim) == FAILURE)
    {
        stop_simulation(sim);
        join_coder_threads(sim);
        return (FAILURE);
    }
    if (join_coder_threads(sim) == FAILURE)
        return (FAILURE);
    return (SUCCESS);
}
