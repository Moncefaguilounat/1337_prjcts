#include "init.h"

static int  init_mutexes(t_simulation *sim)
{
    if (pthread_mutex_init(&sim->log_mutex, NULL) != 0)
        return (FAILURE);
    if (pthread_mutex_init(&sim->simulation_mutex, NULL) != 0)
    {
        pthread_mutex_destroy(&sim->log_mutex);
        return (FAILURE);
    }
    if (pthread_mutex_init(&sim->resource_mutex, NULL) != 0)
    {
        pthread_mutex_destroy(&sim->simulation_mutex);
        pthread_mutex_destroy(&sim->log_mutex);
        return (FAILURE);
    }
    return (SUCCESS);
}

static int  allocate_resources(t_simulation *sim)
{
    sim->coders = malloc(sizeof(t_coder) * sim->number_of_coders);
    if (!sim->coders)
        return (FAILURE);
    sim->dongles = malloc(sizeof(t_dongle) * sim->number_of_coders);
    if (!sim->dongles)
    {
        free(sim->coders);
        sim->coders = NULL;
        return (FAILURE);
    }
    return (SUCCESS);
}

static void reset_simulation(t_simulation *sim)
{
    sim->coders = NULL;
    sim->dongles = NULL;
    sim->simulation_over = 0;
    sim->start_time = 0;
    sim->request_queue.nodes = NULL;
    sim->request_queue.size = 0;
    sim->request_queue.capacity = 0;
    sim->request_queue.next_order = 0;
}

static int prepare_storage(t_simulation *sim)
{
    if (pthread_cond_init(&sim->resource_cond, NULL) != 0)
        return (FAILURE);
    if (heap_init(&sim->request_queue, sim->number_of_coders) == FAILURE)
    {
        pthread_cond_destroy(&sim->resource_cond);
        return (FAILURE);
    }
    if (allocate_resources(sim) == FAILURE)
    {
        heap_destroy(&sim->request_queue);
        pthread_cond_destroy(&sim->resource_cond);
        return (FAILURE);
    }
    return (SUCCESS);
}

int init_simulation(t_simulation *sim)
{
    reset_simulation(sim);
    if (init_mutexes(sim) == FAILURE)
        return (FAILURE);
    if (prepare_storage(sim) == FAILURE)
    {
        pthread_mutex_destroy(&sim->resource_mutex);
        pthread_mutex_destroy(&sim->simulation_mutex);
        pthread_mutex_destroy(&sim->log_mutex);
        return (FAILURE);
    }
    if (init_coder(sim) == FAILURE)
    {
        cleanup_simulation(sim, sim->number_of_coders);
        return (FAILURE);
    }
    if (init_dongles(sim) == FAILURE)
    {
        cleanup_simulation(sim, sim->number_of_coders);
        return (FAILURE);
    }
    return (SUCCESS);
}
