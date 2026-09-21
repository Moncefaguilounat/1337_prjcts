#ifndef SCHEDULER_H
# define SCHEDULER_H

# include "types.h"

int     parent(int i);
int     left_child(int i);
int     right_child(int i);
void    swap(t_heap_node *a, t_heap_node *b);
int     get_smallest_child(t_scheduler *heap, int i);
int     node_precedes(t_heap_node *first, t_heap_node *second);

int     heap_init(t_scheduler *heap, int capacity);
int     heap_insert(t_scheduler *heap, int coder_id, long priority);
int     heap_extract_min(t_scheduler *heap, int *out_coder_id);
int     heap_remove_at(t_scheduler *heap, int index, int *out_coder_id);
void    sift_up(t_scheduler *heap, int i);
void    sift_down(t_scheduler *heap, int i);

void    heap_destroy(t_scheduler *heap);

#endif
