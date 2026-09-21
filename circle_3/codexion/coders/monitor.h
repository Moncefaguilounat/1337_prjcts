#ifndef MONITOR_H
# define MONITOR_H

# include "types.h"
# include "simulation.h"

void    *monitor_routine(void *arg);
void    wait_for_monitor_event(t_simulation *sim);

#endif
