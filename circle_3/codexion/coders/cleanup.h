#ifndef CLEANUP_H
# define CLEANUP_H

# include "types.h"
# include "scheduler.h"

void    cleanup_coders(t_simulation *sim, int i);
void    cleanup_dongles(t_simulation *sim, int i);
void    cleanup_simulation(t_simulation *sim, int i);
void    heap_destroy(t_scheduler *heap);

#endif
