#include "logger.h"

void    log_state(t_simulation *sim, int coder_id, char *message)
{
    long    timestamp;
    int     active;

    pthread_mutex_lock(&sim->log_mutex);
    pthread_mutex_lock(&sim->simulation_mutex);
    active = !sim->simulation_over;
    pthread_mutex_unlock(&sim->simulation_mutex);
    if (active)
    {
        timestamp = get_time_ms(sim) - sim->start_time;
        printf("%ld %d %s\n", timestamp, coder_id, message);
    }
    pthread_mutex_unlock(&sim->log_mutex);
}

void    log_compile_start(t_simulation *sim, int coder_id)
{
    long    timestamp;
    int     active;

    pthread_mutex_lock(&sim->log_mutex);
    pthread_mutex_lock(&sim->simulation_mutex);
    active = !sim->simulation_over;
    pthread_mutex_unlock(&sim->simulation_mutex);
    if (active)
    {
        timestamp = get_time_ms(sim);
        pthread_mutex_lock(&sim->coders[coder_id - 1].coder_mutex);
        sim->coders[coder_id - 1].last_compile_time = timestamp;
        pthread_mutex_unlock(&sim->coders[coder_id - 1].coder_mutex);
        timestamp -= sim->start_time;
        printf("%ld %d has taken a dongle\n", timestamp, coder_id);
        printf("%ld %d has taken a dongle\n", timestamp, coder_id);
        printf("%ld %d is compiling\n", timestamp, coder_id);
    }
    pthread_mutex_unlock(&sim->log_mutex);
}

void    log_burnout(t_simulation *sim, int coder_id)
{
    long    timestamp;

    pthread_mutex_lock(&sim->log_mutex);
    timestamp = get_time_ms(sim) - sim->start_time;
    printf("%ld %d burned out\n", timestamp, coder_id);
    pthread_mutex_unlock(&sim->log_mutex);
}
