#ifndef TYPES_H
# define TYPES_H

# define _DEFAULT_SOURCE
# define _POSIX_C_SOURCE 200809L

# include <pthread.h>
# include <sys/time.h>
# include <time.h>
# include <stdlib.h>
# include <stdio.h>
# include <unistd.h>
# include <string.h>

# define FAILURE 1
# define SUCCESS 0
# define EDF 1
# define FIFO 0

typedef struct s_heap_node
{
    int     coder_id;
    long    priority;
    unsigned long order;
}   t_heap_node;

typedef struct s_scheduler
{
    t_heap_node *nodes;
    int         size;
    int         capacity;
    unsigned long next_order;
}   t_scheduler;

typedef struct s_simulation t_simulation;

typedef struct s_dongle
{
    int                 available;
    long                released_at;
    pthread_mutex_t     mutex;
}   t_dongle;

typedef struct s_coder
{
    int             id;
    pthread_t       thread;
    pthread_mutex_t coder_mutex;
    int             compile_count;
    long            last_compile_time;
    int             left_dongle;
    int             right_dongle;
    int             dongles_reserved;
    t_simulation    *sim;
}   t_coder;

struct s_simulation
{
    int                 number_of_coders;
    long                time_to_burnout;
    long                time_to_compile;
    long                time_to_debug;
    long                time_to_refactor;
    int                 max_compiles;
    long                dongle_cooldown;
    int                 scheduler;
    t_coder             *coders;
    t_dongle            *dongles;
    int                 simulation_over;
    long                start_time;
    pthread_mutex_t     log_mutex;
    pthread_mutex_t     simulation_mutex;
    pthread_mutex_t     resource_mutex;
    pthread_cond_t      resource_cond;
    t_scheduler         request_queue;
    pthread_t           monitor_thread;
};

#endif
