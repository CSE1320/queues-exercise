#include <stdio.h>
#include <stdlib.h>
#include "queue.h"

int main() {
    printf("I am the queue!\n");
    Queue* q = queue_create(10);
    queue_pprint(q);
    queue_destroy(q);

    return 0;
}