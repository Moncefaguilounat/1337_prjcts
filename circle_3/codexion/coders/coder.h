#ifndef CODER_H
# define CODER_H

# include "types.h"
# include "dongle.h"
# include "logger.h"
# include "simulation.h"

int     create_coder_threads(t_simulation *sim);
int     join_coder_threads(t_simulation *sim);
int     init_coder(t_simulation *sim);
void    *coder_routine(void *arg);

#endif
