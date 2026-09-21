#include "coder.h"

int     init_coder(t_simulation *sim)
{
    int     i;
    t_coder *coder;

    i = 0;
    while (i < sim->number_of_coders)
    {
        coder = &sim->coders[i];
        coder->id = i + 1;
        coder->left_dongle = i;
        coder->right_dongle = (i + 1) % sim->number_of_coders;
        coder->dongles_reserved = 0;
        coder->compile_count = 0;
        coder->sim = sim;
        if (pthread_mutex_init(&coder->coder_mutex, NULL) != 0)
        {
            while (--i >= 0)
                pthread_mutex_destroy(&sim->coders[i].coder_mutex);
            return (FAILURE);
        }
        i++;
    }
    return (SUCCESS);
}
