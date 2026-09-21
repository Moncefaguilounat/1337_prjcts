#ifndef SIMULATION_H
# define SIMULATION_H

# include "coder.h"
# include "monitor.h"

void    precise_sleep(long duration_ms, t_simulation *sim);
void    precise_sleep_until(long end, t_simulation *sim);
int     run_simulation(t_simulation *sim);
int     is_simulation_over(t_simulation *sim);
void    stop_simulation(t_simulation *sim);

#endif
