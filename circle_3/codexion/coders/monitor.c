#include "monitor.h"

static int has_burned_out(t_simulation *sim)
{
    int     i;
    long    elapsed;
    t_coder *coder;

    i = 0;
    while (i < sim->number_of_coders)
    {
        coder = &sim->coders[i];
        pthread_mutex_lock(&coder->coder_mutex);
        elapsed = get_time_ms(sim) - coder->last_compile_time;
        if (coder->compile_count < sim->max_compiles
            && elapsed > sim->time_to_burnout)
        {
            pthread_mutex_unlock(&coder->coder_mutex);
            stop_simulation(sim);
            log_burnout(sim, coder->id);
            return (1);
        }
        pthread_mutex_unlock(&coder->coder_mutex);
        i++;
    }
    return (0);
}

static int  all_coders_finished(t_simulation *sim)
{
    int     i;
    t_coder *coder;

    i = 0;
    while (i < sim->number_of_coders)
    {
        coder = &sim->coders[i];
        pthread_mutex_lock(&coder->coder_mutex);
        if (coder->compile_count < sim->max_compiles)
        {
            pthread_mutex_unlock(&coder->coder_mutex);
            return (0);
        }
        pthread_mutex_unlock(&coder->coder_mutex);
        i++;
    }
    return (1);
}

void    *monitor_routine(void *arg)
{
    t_simulation *sim;

    sim = (t_simulation *)arg;
    while (!is_simulation_over(sim))
    {
        if (has_burned_out(sim))
            return (NULL);
        schedule_ready_coders(sim);
        if (all_coders_finished(sim))
        {
            stop_simulation(sim);
            return (NULL);
        }
        wait_for_monitor_event(sim);
    }
    return (NULL);
}
