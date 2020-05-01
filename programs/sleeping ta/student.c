/**
 * General structure of a student.
 *
 */

#include <pthread.h>
#include <stdio.h>
#include <time.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include "ta.h"

void *student_loop(void *param)
{
	int number = *((int *)param);
	int sleep_time;

	//printf("I am student %d\n", number);

	srandom((unsigned)time(NULL));
	sleep_time = (int)((random() % MAX_SLEEP_TIME) + 1);
	while (1) {
		printf("%d will program\n", number);
		programming(sleep_time);
		
		printf("%d would like a seat\n", number);
		pthread_mutex_lock(&seats);
		if (waiting < NUM_OF_SEATS) {
			++waiting;
			pthread_mutex_unlock(&seats);
			printf("%d would like help from the ta\n", number);
			sem_post(&TASem);
			sem_wait(&studentSem);
			printf("%d has gotten help\n", number);
		}
		else pthread_mutex_unlock(&seats);

	}
	return NULL;
}
