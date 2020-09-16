/* time.h Jonathan P Dawson 2015-10-21 */

#ifndef __time_h__
#define __time_h__

#include <stdlib.h>

#define clock_t unsigned long long
#define time_t unsigned long long

typedef struct {
	int tm_sec;   /*  seconds after the minute --- [0, 60] */
	int tm_min;   /*  minutes after the hour --- [0, 59] */
	int tm_hour;  /*  hours since midnight --- [0, 23] */
	int tm_mday;  /*  day of the month --- [1, 31] */
	int tm_mon;   /*  months since January --- [0, 11] */
	int tm_year;  /*  years since 1900 */
	int tm_wday;  /*  days since Sunday --- [0, 6] */
	int tm_yday;  /*  days since January 1 --- [0, 365] */
	int tm_isdst; /*  Daylight Saving Time flag */
} tm;

clock_t clock();
double difftime(time_t time1, time_t time0);
time_t human_to_unix(tm human);
time_t mktime(tm *timeptr);
time_t time(time_t *timer);
void set_time(time_t t);
char *asctime(tm *timeptr);
tm unix_to_human(time_t unix_time);
tm *gmtime(time_t *timer);
tm *localtime(time_t *timer);

#endif