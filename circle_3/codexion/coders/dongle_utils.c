#include "dongle.h"

long    get_priority(t_coder *coder)
{
    long    deadline;


    if (coder->sim->scheduler == EDF)
    {
        deadline = coder->last_compile_time + coder->sim->time_to_burnout;
        return (deadline);
    }
    return (get_time_ms(coder->sim));
}
