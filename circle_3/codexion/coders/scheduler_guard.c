#include "dongle.h"

int candidate_blocks_earlier(t_simulation *sim, int coder_id)
{
    t_coder *candidate;
    t_coder *first;
    long    now;

    if (sim->request_queue.size == 0
        || sim->request_queue.nodes[0].coder_id == coder_id)
        return (0);
    first = &sim->coders[sim->request_queue.nodes[0].coder_id - 1];
    candidate = &sim->coders[coder_id - 1];
    if (!sim->dongles[first->left_dongle].available
        || !sim->dongles[first->right_dongle].available)
        return (0);
    now = get_time_ms(sim);
    if (now - sim->dongles[first->left_dongle].released_at
        < sim->dongle_cooldown || now - sim->dongles[first->right_dongle]
        .released_at < sim->dongle_cooldown)
        return (candidate->left_dongle == first->left_dongle
        || candidate->left_dongle == first->right_dongle
        || candidate->right_dongle == first->left_dongle
        || candidate->right_dongle == first->right_dongle);
    return (0);
}
