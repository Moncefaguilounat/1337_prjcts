#include "monitor.h"

static long next_burnout(t_simulation *sim)
{
    long    event;
    long    next;
    int     i;

    next = -1;
    i = 0;
    while (i < sim->number_of_coders)
    {
        pthread_mutex_lock(&sim->coders[i].coder_mutex);
        event = sim->coders[i].last_compile_time
            + sim->time_to_burnout + 1;
        pthread_mutex_unlock(&sim->coders[i].coder_mutex);
        if (next < 0 || event < next)
            next = event;
        i++;
    }
    return (next);
}

static long coder_ready_at(t_simulation *sim, t_coder *coder)
{
    long    left_ready;
    long    right_ready;

    if (coder->left_dongle == coder->right_dongle
        || !sim->dongles[coder->left_dongle].available
        || !sim->dongles[coder->right_dongle].available)
        return (-1);
    left_ready = sim->dongles[coder->left_dongle].released_at
        + sim->dongle_cooldown;
    right_ready = sim->dongles[coder->right_dongle].released_at
        + sim->dongle_cooldown;
    if (left_ready > right_ready)
        return (left_ready);
    return (right_ready);
}

static long next_cooldown(t_simulation *sim, long now)
{
    t_coder *coder;
    long    ready;
    long    next;
    int     i;

    next = -1;
    i = 0;
    while (i < sim->request_queue.size)
    {
        coder = &sim->coders[sim->request_queue.nodes[i].coder_id - 1];
        ready = coder_ready_at(sim, coder);
        if (ready >= now && (next < 0 || ready < next))
            next = ready;
        i++;
    }
    return (next);
}

static void spin_until(t_simulation *sim, long wake_time)
{
    while (!is_simulation_over(sim) && get_time_ms(sim) < wake_time)
    {
    }
}

void    wait_for_monitor_event(t_simulation *sim)
{
    long            wake_time;
    long            cooldown;
    long            now;

    wake_time = next_burnout(sim);
    pthread_mutex_lock(&sim->resource_mutex);
    now = get_time_ms(sim);
    cooldown = next_cooldown(sim, now);
    if (cooldown >= 0 && cooldown < wake_time)
        wake_time = cooldown;
    pthread_mutex_unlock(&sim->resource_mutex);
    now = get_time_ms(sim);
    if (!is_simulation_over(sim) && wake_time - now > 1)
        usleep(100);
    if (wake_time > now && wake_time - now <= 1)
        spin_until(sim, wake_time);
}
