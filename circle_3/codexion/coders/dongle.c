#include "dongle.h"

int     init_dongle(t_simulation *sim, int index)
{
    t_dongle    *dongle;

    dongle = &sim->dongles[index];
    dongle->available = 1;
    dongle->released_at = 0;
    if (pthread_mutex_init(&dongle->mutex, NULL) != 0)
        return (FAILURE);
    return (SUCCESS);
}

int     init_dongles(t_simulation *sim)
{
    int i;

    i = 0;
    while (i < sim->number_of_coders)
    {
        if (init_dongle(sim, i) != SUCCESS)
        {
            cleanup_dongles(sim, i);
            return (FAILURE);
        }
        i++;
    }
    return (SUCCESS);
}

void    release_dongle(t_coder *coder, int dongle_index)
{
    t_simulation    *sim;
    t_dongle        *dongle;

    sim = coder->sim;
    dongle = &sim->dongles[dongle_index];
    pthread_mutex_lock(&sim->resource_mutex);
    pthread_mutex_lock(&dongle->mutex);
    dongle->available = 1;
    dongle->released_at = get_time_ms(sim);
    pthread_mutex_unlock(&dongle->mutex);
    pthread_cond_broadcast(&sim->resource_cond);
    pthread_mutex_unlock(&sim->resource_mutex);
}

int acquire_both_dongles(t_coder *coder)
{
    t_simulation *sim;

    sim = coder->sim;
    pthread_mutex_lock(&sim->resource_mutex);
    coder->dongles_reserved = 0;
    if (heap_insert(&sim->request_queue, coder->id,
            get_priority(coder)) == FAILURE)
        return (pthread_mutex_unlock(&sim->resource_mutex), FAILURE);
    pthread_cond_broadcast(&sim->resource_cond);
    while (!coder->dongles_reserved && !is_simulation_over(sim))
        pthread_cond_wait(&sim->resource_cond, &sim->resource_mutex);
    pthread_mutex_unlock(&sim->resource_mutex);
    if (is_simulation_over(sim))
        return (FAILURE);
    return (SUCCESS);
}
