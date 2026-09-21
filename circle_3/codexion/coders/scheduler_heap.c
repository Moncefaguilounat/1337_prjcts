#include "scheduler.h"

int get_smallest_child(t_scheduler *heap, int i)
{
    int smallest;
    int left;
    int right;

    left = left_child(i);
    right = right_child(i);
    smallest = i;
    if (left < heap->size
        && node_precedes(&heap->nodes[left], &heap->nodes[smallest]))
        smallest = left;
    if (right < heap->size
        && node_precedes(&heap->nodes[right], &heap->nodes[smallest]))
        smallest = right;
    return (smallest);
}

void sift_up(t_scheduler *heap, int index)
{
    int parent_index;

    while (index > 0)
    {
        parent_index = parent(index);
        if (!node_precedes(&heap->nodes[index], &heap->nodes[parent_index]))
            break ;
        swap(&heap->nodes[index], &heap->nodes[parent_index]);
        index = parent_index;
    }
}

void sift_down(t_scheduler *heap, int index)
{
    int smallest;

    while (1)
    {
        smallest = get_smallest_child(heap, index);
        if (smallest == index)
            break ;
        swap(&heap->nodes[index], &heap->nodes[smallest]);
        index = smallest;
    }
}
