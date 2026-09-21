#include "scheduler.h"

int heap_init(t_scheduler *heap, int capacity)
{
    heap->nodes = malloc(sizeof(t_heap_node) * capacity);
    if (!heap->nodes)
        return (FAILURE);
    heap->size = 0;
    heap->capacity = capacity;
    heap->next_order = 0;
    return (SUCCESS);
}

int heap_insert(t_scheduler *heap, int coder_id, long priority)
{
    if (heap->size >= heap->capacity)
        return (FAILURE);
    heap->nodes[heap->size].coder_id = coder_id;
    heap->nodes[heap->size].priority = priority;
    heap->nodes[heap->size].order = heap->next_order++;
    heap->size++;
    sift_up(heap, heap->size - 1);
    return (SUCCESS);
}

int heap_extract_min(t_scheduler *heap, int *out_coder_id)
{
    if (heap->size == 0)
        return (FAILURE);
    *out_coder_id = heap->nodes[0].coder_id;
    heap->size--;
    if (heap->size > 0)
    {
        heap->nodes[0] = heap->nodes[heap->size];
        sift_down(heap, 0);
    }
    return (SUCCESS);
}

int heap_remove_at(t_scheduler *heap, int index, int *out_coder_id)
{
    int parent_index;

    if (index < 0 || index >= heap->size)
        return (FAILURE);
    *out_coder_id = heap->nodes[index].coder_id;
    heap->size--;
    if (index == heap->size)
        return (SUCCESS);
    heap->nodes[index] = heap->nodes[heap->size];
    parent_index = parent(index);
    if (index > 0
        && node_precedes(&heap->nodes[index], &heap->nodes[parent_index]))
        sift_up(heap, index);
    else
        sift_down(heap, index);
    return (SUCCESS);
}
