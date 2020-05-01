/**
 * General structure of the teaching assistant.
 *
 */

#include <pthread.h>
#include <stdio.h>
#include <time.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include "ta.h"

void *ta_loop(void *param)
{
	//printf("I am the TA\n");
	srandom((unsigned)time(NULL));

	while (1) {
		int sleep_time = (int)((random() % MAX_SLEEP_TIME) + 1);
		//wait on student semaphore
		printf("TA is waiting for students\n");
		sem_wait(&TASem);
		//help student (--waiting), number of waiting students decreases by 1
		help_student(sleep_time);
		pthread_mutex_lock(&seats);
		waiting--;
		pthread_mutex_unlock(&seats);
		//alert ta semaphore that ta is available to help again
		sem_post(&studentSem);
	}
}
