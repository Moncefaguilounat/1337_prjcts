#ifndef DONGLE_H
# define DONGLE_H

# include "logger.h"
# include "cleanup.h"
# include "simulation.h"

int     init_dongles(t_simulation *sim);
int     acquire_both_dongles(t_coder *coder);
void    schedule_ready_coders(t_simulation *sim);
void    release_dongle(t_coder *coder, int idex_dongle);
long    get_priority(t_coder *coder);
int     candidate_blocks_earlier(t_simulation *sim, int coder_id);

#endif
