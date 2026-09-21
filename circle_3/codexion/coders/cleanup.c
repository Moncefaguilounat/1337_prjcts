#include "cleanup.h"

void    heap_destroy(t_scheduler *heap)
{
    if (heap->nodes)
    {
        free(heap->nodes);
        heap->nodes = NULL;
    }
    heap->size = 0;
    heap->capacity = 0;
}

void    cleanup_coders(t_simulation *sim, int i)
{
    if (!sim->coders)
        return ;
    while (--i >= 0)
        pthread_mutex_destroy(&sim->coders[i].coder_mutex);
}

void    cleanup_dongles(t_simulation *sim, int i)
{
    if (!sim->dongles)
        return ;
    while (--i >= 0)
    {
        pthread_mutex_destroy(&sim->dongles[i].mutex);
    }
}

void    cleanup_simulation(t_simulation *sim, int i)
{
    cleanup_dongles(sim, i);
    cleanup_coders(sim, i);
    if (sim->dongles)
        free(sim->dongles);
    if (sim->coders)
        free(sim->coders);
    sim->dongles = NULL;
    sim->coders = NULL;
    heap_destroy(&sim->request_queue);
    pthread_cond_destroy(&sim->resource_cond);
    pthread_mutex_destroy(&sim->resource_mutex);
    pthread_mutex_destroy(&sim->log_mutex);
    pthread_mutex_destroy(&sim->simulation_mutex);
}
