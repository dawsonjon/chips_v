/* time.h Jonathan P Dawson 2015-10-21 */

#ifndef __time_h__
#define __time_h__

#include <stdlib.h>

#define clock_t unsigned long long
#define time_t unsigned long long
extern const unsigned CLOCKS_PER_SEC;

struct tm {
	int tm_sec;   /*  seconds after the minute --- [0, 60] */
	int tm_min;   /*  minutes after the hour --- [0, 59] */
	int tm_hour;  /*  hours since midnight --- [0, 23] */
	int tm_mday;  /*  day of the month --- [1, 31] */
	int tm_mon;   /*  months since January --- [0, 11] */
	int tm_year;  /*  years since 1900 */
	int tm_wday;  /*  days since Sunday --- [0, 6] */
	int tm_yday;  /*  days since January 1 --- [0, 365] */
	int tm_isdst; /*  Daylight Saving Time flag */
};

/*
The clock function

Synopsis

         #include <time.h>
         clock_t clock(void);

Description

   The clock function determines the processor time used.  

Returns

   The clock function returns the implementation's best approximation
to the processor time used by the program since the beginning of an
implementation-defined era related only to the program invocation.  To
determine the time in seconds, the value returned by the clock
function should be divided by the value of the macro CLK_TCK .  If the
processor time used is not available or its value cannot be
represented, the function returns the value (clock_t)-1 .
*/

clock_t clock();

/*
The difftime function

Synopsis

         #include <time.h>
         double difftime(time_t time1, time_t time0);

Description

   The difftime function computes the difference between two calendar
times: time1 - time0 .

Returns

   The difftime function returns the difference expressed in seconds
as a double .

*/

double difftime(time_t time1, time_t time0);

/*
 *
The mktime function

Synopsis

         #include <time.h>
         time_t mktime(struct tm *timeptr);

Description

   The mktime function converts the broken-down time, expressed as
local time, in the structure pointed to by timeptr into a calendar
time value with the same encoding as that of the values returned by
the time function.  The original values of the tm_wday and tm_yday
components of the structure are ignored, and the original values of
the other components are not restricted to the ranges indicated
above./124/ On successful completion, the values of the tm_wday and
tm_yday components of the structure are set appropriately, and the
other components are set to represent the specified calendar time, but
with their values forced to the ranges indicated above; the final
value of tm_mday is not set until tm_mon and tm_year are determined.

Returns

   The mktime function returns the specified calendar time encoded as
a value of type time_t .  If the calendar time cannot be represented,
the function returns the value (time_t)-1 .

Example

   What day of the week is July 4, 2001? 
   

         #include <stdio.h>
         #include <time.h>
         static const char *const wday[] = {
                  "Sunday", "Monday", "Tuesday", "Wednesday",
                  "Thursday", "Friday", "Saturday", "-unknown-"
         };
         struct tm time_str;



         time_str.tm_year   = 2001 - 1900;
         time_str.tm_mon    = 7 - 1;
         time_str.tm_mday   = 4;
         time_str.tm_hour   = 0;
         time_str.tm_min    = 0;
         time_str.tm_sec    = 1;
         time_str.tm_isdst  = -1;
         if (mktime(&time_str) == -1)
                  time_str.tm_wday = 7;
         printf("%s\n", wday[time_str.tm_wday]);

*/

time_t mktime(struct tm *timeptr);

/*
The time function

Synopsis

         #include <time.h>
         time_t time(time_t *timer);

Description

   The time function determines the current calendar time.  The
encoding of the value is unspecified.

Returns

   The time function returns the implementation's best approximation
to the current calendar time.  The value (time_t)-1 is returned if the
calendar time is not available.  If timer is not a null pointer, the
return value is also assigned to the object it points to.

*/

time_t time(time_t *timer);

/*
The set_time function

Synopsis

         #include <time.h>
         void set_time(time_t t);

Description

   The set_time function sets the current system clock time. 

*/

void set_time(time_t t);

/*
The asctime function

Synopsis

         #include <time.h>
         char *asctime(const struct tm *timeptr);

Description

   The asctime function converts the broken-down time in the structure
pointed to by timeptr into a string in the form

         Sun Sep 16 01:03:52 1973\n\0

using the equivalent of the following algorithm.  

char *asctime(const struct tm *timeptr)
{
         static const char wday_name[7][3] = {
                  "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
         };
         static const char mon_name[12][3] = {
                  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
         };
         static char result[26];

         sprintf(result, "%.3s %.3s%3d %.2d:%.2d:%.2d %d\n",
                  wday_name[timeptr->tm_wday],
                  mon_name[timeptr->tm_mon],
                  timeptr->tm_mday, timeptr->tm_hour,
                  timeptr->tm_min, timeptr->tm_sec,
                  1900 + timeptr->tm_year);
         return result;
}

Returns

   The asctime function returns a pointer to the string.  

*/

char *asctime(const struct tm *timeptr);

/*
The ctime function

Synopsis

         #include <time.h>
         char *ctime(const time_t *timer);

Description

   The ctime function converts the calendar time pointed to by timer to local time in the form of a string.  It is equivalent to 

         asctime(localtime(timer))

Returns

   The ctime function returns the pointer returned by the asctime
function with that broken-down time as argument.

*/

char *ctime(const time_t * timer);

/*
The gmtime function

Synopsis

         #include <time.h>
         struct tm *gmtime(const time_t *timer);

Description

   The gmtime function converts the calendar time pointed to by timer
into a broken-down time, expressed as Coordinated Universal Time
(UTC).

Returns

   The gmtime function returns a pointer to that object, or a null
pointer if UTC is not available.
*/

struct tm *gmtime(time_t *timer);

/*

The localtime function

Synopsis

         #include <time.h>
         struct tm *localtime(const time_t *timer);

Description

   The localtime function converts the calendar time pointed to by
timer into a broken-down time, expressed as local time.

Returns

   The localtime function returns a pointer to that object.  

*/

struct tm *localtime(const time_t *timer);

struct tm unix_to_human(time_t unix_time);
time_t human_to_unix(struct tm human);

#endif
