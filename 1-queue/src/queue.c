#include "queue.h"



void queue_reset(Queue* queue){
    q->head = q->data;
    q->tail = q->data;
}

Queue* queue_create(int capacity){
    assert(capacity > 0);
    Queue* q = (Queue*) malloc(sizeof(Queue));
    q->data = (int*) malloc(capacity * sizeof(int));

    // error handling malloc

    queue_reset(q);
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
    // check queue size -- if full, return false; fprintf --> Overflow
    *(queue->tail) = value; //*(0x1213930909) = value
    queue->tail++;
    return true;
}

int queue_dequeue(Queue* queue){
    // check queue size -- if empty, exit underflow message
    int data = *(queue->head); // *(0x1283919);
    *(queue->head) = -1;
    queue->head++;
    if(queue->head == queue->tail){
        queue_reset(queue);
    }
    return -1;
}

bool queue_is_empty(Queue* queue){
    return queue->head == queue->tail;
}
bool queue_is_full(Queue* queue){
    return (queue->tail - queue->head) == queue->capacity;
}