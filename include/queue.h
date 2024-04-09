#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

// Queue structure
typedef struct {
    int* data; // potential for dynamic memory allocation
    int* head;
    // int* tail; // for dequeues
    int size;
    int capacity;
} Queue;


// Function prototypes
queue_create(int capacity);
queue_destroy(Queue* queue);
queue_pprint(Queue* queue);
queue_enqueue(Queue* queue, int value);
queue_dequeue(Queue* queue);
queue_is_empty(Queue* queue);
queue_is_full(Queue* queue);
queue_peek(Queue* queue);
queue_resize(Queue* queue);

