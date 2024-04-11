#include "queue.h"

Queue* queue_create(int capacity){
    assert(capacity > 0);
    Queue* q = (Queue*) malloc(sizeof(Queue));
    q->data = (int*) malloc(capacity * sizeof(int));

    // error handling malloc

    q->head = q->data;
    q->tail = q->data;
    q->capacity = capacity;  
    return q; 
}

void queue_destroy(Queue* queue){
    free(queue->data);
    free(queue);
}

void queue_pprint(Queue* queue){
    printf("Capacity:  %d\n", queue->capacity);
    printf("Head: %p\n", (void*) queue->head);
    printf("Tail: %p\n", (void*) queue->tail);
    printf("Start of Data: %p\n", (void*) queue->data);
    
    for(int i = 0; i < queue->capacity; i++){
        printf(" %d: %d\n", i, queue->data[i]);
    }
}

bool queue_enqueue(Queue* queue, int value){
    
}