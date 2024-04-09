#ifndef QUEUE_H
#define QUEUE_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

// Queue structure
typedef struct {
    int* data; // potential for dynamic memory allocation
    // int data[100];// static memory
    int* head;
    int* tail;
    int capacity;
} Queue;


// Function prototypes
Queue* queue_create(int capacity);
void queue_destroy(Queue* queue);

void queue_pprint(Queue* queue);

bool queue_enqueue(Queue* queue, int value);
int queue_dequeue(Queue* queue);

bool queue_is_empty(Queue* queue);
bool queue_is_full(Queue* queue);

int queue_peek(Queue* queue);
void queue_resize(Queue* queue);

#endif
