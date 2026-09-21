#include "dongle.h"

static int coder_can_compile(t_simulation *sim, int coder_id)
{
    t_coder *coder;
    int     left;
    int     right;
    long    now;

    coder = &sim->coders[coder_id - 1];
    left = coder->left_dongle;
    right = coder->right_dongle;
    if (left == right || !sim->dongles[left].available
        || !sim->dongles[right].available)
        return (0);
    now = get_time_ms(sim);
    if (now - sim->dongles[left].released_at < sim->dongle_cooldown)
        return (0);
    return (now - sim->dongles[right].released_at >= sim->dongle_cooldown);
}

static int next_ready_coder(t_simulation *sim)
{
    int best;
    int i;

    best = -1;
    i = 0;
    while (i < sim->request_queue.size)
    {
        if (coder_can_compile(sim, sim->request_queue.nodes[i].coder_id)
            && !candidate_blocks_earlier(sim,
                sim->request_queue.nodes[i].coder_id)
            && (best < 0 || node_precedes(&sim->request_queue.nodes[i],
                    &sim->request_queue.nodes[best])))
            best = i;
        i++;
    }
    return (best);
}

static void reserve_dongles(t_coder *coder)
{
    t_simulation *sim;
    int         left;
    int         right;
    int         temp;

    sim = coder->sim;
    left = coder->left_dongle;
    right = coder->right_dongle;
    if (left > right)
    {
        temp = left;
        left = right;
        right = temp;
    }
    pthread_mutex_lock(&sim->dongles[left].mutex);
    pthread_mutex_lock(&sim->dongles[right].mutex);
    sim->dongles[left].available = 0;
    sim->dongles[right].available = 0;
    pthread_mutex_unlock(&sim->dongles[right].mutex);
    pthread_mutex_unlock(&sim->dongles[left].mutex);
}

static void grant_coder(t_simulation *sim, int selected)
{
    t_coder *coder;
    int     winner_id;

    winner_id = sim->request_queue.nodes[selected].coder_id;
    heap_remove_at(&sim->request_queue, selected, &winner_id);
    coder = &sim->coders[winner_id - 1];
    reserve_dongles(coder);
    log_compile_start(sim, winner_id);
    coder->dongles_reserved = 1;
}

void schedule_ready_coders(t_simulation *sim)
{
    int     selected;
    int     granted;

    pthread_mutex_lock(&sim->resource_mutex);
    granted = 0;
    selected = next_ready_coder(sim);
    while (selected >= 0)
    {
        grant_coder(sim, selected);
        granted = 1;
        selected = next_ready_coder(sim);
    }
    if (granted)
        pthread_cond_broadcast(&sim->resource_cond);
    pthread_mutex_unlock(&sim->resource_mutex);
}
