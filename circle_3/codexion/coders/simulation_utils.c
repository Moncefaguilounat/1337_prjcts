#include "simulation.h"

void    precise_sleep_until(long end, t_simulation *sim)
{
    long    remaining;

    remaining = end - get_time_ms(sim);
    while (!is_simulation_over(sim) && remaining > 1)
    {
        usleep((remaining - 1) * 1000);
        remaining = end - get_time_ms(sim);
    }
    while (!is_simulation_over(sim) && get_time_ms(sim) < end)
    {
    }
}

void    precise_sleep(long duration_ms, t_simulation *sim)
{
    precise_sleep_until(get_time_ms(sim) + duration_ms, sim);
}

int     is_simulation_over(t_simulation *sim)
{
    int value;

    pthread_mutex_lock(&sim->simulation_mutex);
    value = sim->simulation_over;
    pthread_mutex_unlock(&sim->simulation_mutex);
    return (value);
}

void    stop_simulation(t_simulation *sim)
{
    pthread_mutex_lock(&sim->simulation_mutex);
    if (sim->simulation_over)
    {
        pthread_mutex_unlock(&sim->simulation_mutex);
        return;
    }
    sim->simulation_over = 1;
    pthread_mutex_unlock(&sim->simulation_mutex);
    pthread_mutex_lock(&sim->resource_mutex);
    pthread_cond_broadcast(&sim->resource_cond);
    pthread_mutex_unlock(&sim->resource_mutex);
}
