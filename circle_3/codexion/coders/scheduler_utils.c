#include "scheduler.h"

int  parent(int i)
{
    return ((i - 1) / 2);
}

int  left_child(int i)
{
    return ((i * 2) + 1);
}

int  right_child(int i)
{
    return ((i * 2) + 2);
}

void swap(t_heap_node *a, t_heap_node *b)
{
    t_heap_node tmp;

    tmp = *a;
    *a = *b;
    *b = tmp;
}

int node_precedes(t_heap_node *first, t_heap_node *second)
{
    if (first->priority != second->priority)
        return (first->priority < second->priority);
    return (first->order < second->order);
}
