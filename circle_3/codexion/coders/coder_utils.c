#include "coder.h"

static void wait_for_request(t_simulation *sim, int expected)
{
    int queued;

    queued = 0;
    while (queued < expected)
    {
        pthread_mutex_lock(&sim->resource_mutex);
        queued = sim->request_queue.size;
        pthread_mutex_unlock(&sim->resource_mutex);
        if (queued < expected)
            usleep(100);
    }
}

int     create_coder_threads(t_simulation *sim)
{
    int i;

    i = 0;
    while (i < sim->number_of_coders)
    {
        if (pthread_create(&sim->coders[i].thread,
                          NULL, coder_routine, &sim->coders[i]) != 0)
        {
            stop_simulation(sim);
            while (--i >= 0)
                pthread_join(sim->coders[i].thread, NULL);
            return (FAILURE);
        }
        i++;
        wait_for_request(sim, i);
    }
    return (SUCCESS);
}

int     join_coder_threads(t_simulation *sim)
{
    int i;

    i = 0;
    while (i < sim->number_of_coders)
    {
        if (pthread_join(sim->coders[i].thread, NULL) != 0)
            return (FAILURE);
        i++;
    }
    return (SUCCESS);
}

long    get_time_ms(t_simulation *sim)
{
    struct timeval  tv;

    (void)sim;
    gettimeofday(&tv, NULL);
    return (tv.tv_sec * 1000 + tv.tv_usec / 1000);
}
