#ifndef LOGGER_H
# define LOGGER_H

# include "types.h"

long    get_time_ms(t_simulation *sim);
void    log_state(t_simulation *sim, int coder_id, char *message);
void    log_compile_start(t_simulation *sim, int coder_id);
void    log_burnout(t_simulation *sim, int coder_id);

#endif
