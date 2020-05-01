/**
 * Header file for sleeping TA
 */

#include <pthread.h>
#include <semaphore.h>

// the maximum time (in seconds) to sleep
#define MAX_SLEEP_TIME	5

// number of maximum waiting students
#define MAX_WAITING_STUDENTS	3

// number of potential students
#define NUM_OF_STUDENTS		5

// number of available seats
#define NUM_OF_SEATS	3

//number of students waiting
int waiting;

//mutex for seats
pthread_mutex_t seats;

//semaphore for signaling TA that student has arrived
//value of semaphore represents number of students being helped (maximum of 1)
sem_t TASem;

//semaphore for signaling waiting students that the TA can help
//value of semaphore represents number of students waiting (maximum of NUM_OF_SEATS)
sem_t studentSem;

// the numeric id of each student
int student_id[NUM_OF_STUDENTS];

// student function prototype
void *student_loop(void *param);

// ta function prototype
void *ta_loop(void *param);

// simulate programming
void programming(int sleeptime);

// simulate helping a student
void help_student(int sleeptime);
