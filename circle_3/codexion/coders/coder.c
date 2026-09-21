#include "coder.h"

static int compile(t_coder *coder)
{
    long    started_at;

    if (acquire_both_dongles(coder) == FAILURE)
        return (FAILURE);
    pthread_mutex_lock(&coder->coder_mutex);
    started_at = coder->last_compile_time;
    pthread_mutex_unlock(&coder->coder_mutex);
    precise_sleep_until(started_at + coder->sim->time_to_compile,
        coder->sim);
    release_dongle(coder, coder->right_dongle);
    release_dongle(coder, coder->left_dongle);
    pthread_mutex_lock(&coder->coder_mutex);
    coder->compile_count++;
    pthread_mutex_unlock(&coder->coder_mutex);
    return (SUCCESS);
}

static void debug(t_coder *coder)
{
    if (is_simulation_over(coder->sim))
        return ;
    log_state(coder->sim, coder->id, "is debugging");
    precise_sleep(coder->sim->time_to_debug, coder->sim);
}

static void refactor(t_coder *coder)
{
    if (is_simulation_over(coder->sim))
        return ;
    log_state(coder->sim, coder->id, "is refactoring");
    precise_sleep(coder->sim->time_to_refactor, coder->sim);
}

static int coder_finished(t_coder *coder)
{
    int finished;

    pthread_mutex_lock(&coder->coder_mutex);
    finished = (coder->compile_count >= coder->sim->max_compiles);
    pthread_mutex_unlock(&coder->coder_mutex);
    return (finished);
}

void    *coder_routine(void *arg)
{
    t_coder *coder;

    coder = (t_coder *)arg;
    while (!is_simulation_over(coder->sim) && !coder_finished(coder))
    {
        if (compile(coder) == FAILURE)
            return (NULL);
        debug(coder);
        refactor(coder);
    }
    return (NULL);
}
