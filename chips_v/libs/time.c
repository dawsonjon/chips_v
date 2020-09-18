/* time.h Jonathan P Dawson 2015-10-21 */

#include <time.h>

static int tz_offset = 0;

static int _is_dst_human(struct tm human){

  time_t end_of_dst;
  struct tm last_sunday_in_october;
  /*start at end of October*/
  last_sunday_in_october.tm_year = human.tm_year;
  last_sunday_in_october.tm_mon = 9;
  last_sunday_in_october.tm_mday = 31;
  last_sunday_in_october.tm_hour = 1; /*2 o'clock DST == 1 o'clock UTC*/
  last_sunday_in_october.tm_min = 0;
  last_sunday_in_october.tm_sec = 0;
  last_sunday_in_october.tm_isdst = 0;
  end_of_dst = human_to_unix(last_sunday_in_october);
  last_sunday_in_october = unix_to_human(end_of_dst);
  /*subtract the weekday to find the previous Sunday*/
  last_sunday_in_october.tm_mday -= last_sunday_in_october.tm_wday;
  end_of_dst = human_to_unix(last_sunday_in_october);

  time_t start_of_dst;
  struct tm last_sunday_in_march;
  /*start at end of March*/
  last_sunday_in_march.tm_year = human.tm_year;
  last_sunday_in_march.tm_mon = 2;
  last_sunday_in_march.tm_mday = 31;
  last_sunday_in_march.tm_hour = 1;
  last_sunday_in_march.tm_min = 0;
  last_sunday_in_march.tm_sec = 0;
  last_sunday_in_october.tm_isdst = 0;
  start_of_dst = human_to_unix(last_sunday_in_march);
  last_sunday_in_march = unix_to_human(start_of_dst);
  /*subtract the weekday to find the previous Sunday*/
  last_sunday_in_march.tm_mday -= last_sunday_in_march.tm_wday;
  start_of_dst = human_to_unix(last_sunday_in_march);

  time_t unix_time = human_to_unix(human);
  return start_of_dst <= unix_time && unix_time < end_of_dst;

}

static int _is_dst_unix(time_t unix_time){

  return _is_dst_human(unix_to_human(unix_time));

}


clock_t clock(){
    volatile clock_t* timer = (clock_t *) 0x80000000;
    volatile clock_t* timer_hi = (clock_t *) 0x80000004;

    return *timer | (*timer_hi << 32);
}


double difftime(time_t time1, time_t time0){
	return time1 - time0;
}

static unsigned _is_leap_year(unsigned year){
    return year%4==0 && (year%100!=0 || year%400==0);
}

static unsigned _days_in_year(unsigned year){
    return _is_leap_year(year) ? 366 : 365;
}

static unsigned _days_in_month(unsigned year, unsigned month){
    if (month == 3 || month == 8 || month == 5 || month == 10) return 30;
    if (month == 1) return _is_leap_year(year) ? 29 : 28;
    return 31;
}

time_t human_to_unix(struct tm human){
    time_t unix_time;
    unsigned year, month, temp;

    unix_time = 0;
    year = 1970;
    temp = human.tm_year;
    while(1){
        if(year == temp+1900) break;
        unix_time += _days_in_year(year) * 86400;
	year++;
    }
    month = 0;
    while(1){
        if(month == human.tm_mon) break;
        unix_time += _days_in_month(year, month) * 86400;
	month++;
    }
    unix_time += (human.tm_mday - 1) * 86400;
    unix_time += human.tm_hour * 3600;
    unix_time += human.tm_min * 60;
    unix_time += human.tm_sec;

    return unix_time;
}

time_t mktime(struct tm *timeptr){

    struct tm human;
    time_t unix_time, local_time;

    human = *timeptr;
    unix_time = human_to_unix(human);

    if (human.tm_isdst > 0){
        /*daylight saving is in effect*/
        local_time = unix_time - 3600;
    } else if (human.tm_isdst < 0){
        /*automatically determine*/
        local_time = unix_time - (_is_dst_human(human)?3600:0);
    } else {
        /*daylight saving time not in effect*/
        local_time = unix_time;
    }

    local_time -= tz_offset;
    *timeptr = unix_to_human(local_time);

    if (human.tm_isdst > 0){
        timeptr->tm_isdst=1;
    } else if (human.tm_isdst < 0){
        timeptr->tm_isdst=_is_dst_human(human);
    } else {
        timeptr->tm_isdst=0;
    }

    return local_time;

}

static time_t set_time_ = 0;
time_t time(time_t *timer){

    unsigned long t;

    /*calculate uptime in seconds*/
    t = clock()/CLOCKS_PER_SEC;

    /*convert uptime to calendar time*/
    t += set_time_;

    if (timer != (time_t*)NULL) {
	*timer = t;
    }

    return t;

}

void set_time(time_t t) {
   time_t up_time = clock()/CLOCKS_PER_SEC;
   set_time_ = t - up_time;
}

static char result_[26];
char *asctime(const struct tm *timeptr)
{
         const char wday_name[] = "SunMonTueWedThuFriSat";
         const char mon_name[] = "JanFebMarAprMayJunJulAugSepOctNovDec" ;
	 int i;
	 div_t ret;

	 for (i=0; i<3; i++){
	   result_[i] = wday_name[timeptr->tm_wday*3 + i];
         }
	 result_[3] = ' ';

	 for (i=0; i<3; i++){
	   result_[i+4] = mon_name[timeptr->tm_mon*3 + i];
         }
	 result_[7] = ' ';

	 ret = div(timeptr->tm_mday, 10);
	 result_[8] = ret.quot + '0';
	 result_[9] = ret.rem + '0';
	 result_[10] = ' ';

	 ret = div(timeptr->tm_hour, 10);
	 result_[11] = ret.quot + '0';
	 result_[12] = ret.rem + '0';
	 result_[13] = ':';
	 ret = div(timeptr->tm_min, 10);
	 result_[14] = ret.quot + '0';
	 result_[15] = ret.rem + '0';
	 result_[16] = ':';
	 ret = div(timeptr->tm_sec, 10);
	 result_[17] = ret.quot + '0';
	 result_[18] = ret.rem + '0';
	 result_[19] = ' ';

	 ret = div(timeptr->tm_year + 1900, 1000);
	 result_[20] = ret.quot + '0';
         ret = div(ret.rem, 100); 
	 result_[21] = ret.quot + '0';
         ret = div(ret.rem, 10); 
	 result_[22] = ret.quot + '0';
	 result_[23] = ret.rem + '0';
	 result_[24] = '\n';
	 result_[25] = 0;

         return result_;
}

char * ctime(const time_t * timer){
    return asctime(localtime(timer));
}

/* Convert Unix time to broken down time*/
struct tm unix_to_human(time_t unix_time){

    struct tm human;
    unsigned temp, days;
    div_t res;

    human.tm_year = 1970;
    human.tm_wday = 4;
    while(1){
        days = _days_in_year(human.tm_year);
        temp = days * 86400;
        if(temp > unix_time) break;
        human.tm_year++;
        human.tm_wday+=days;
        unix_time-=temp;
    }

    human.tm_mon = 0;
    human.tm_yday = 0;
    while(1){
        days = _days_in_month(human.tm_year, human.tm_mon);
        temp = days * 86400;
        if(temp > unix_time) break;
        human.tm_mon++;
        human.tm_wday+=days;
        human.tm_yday+=days;
        unix_time -= temp;
    }
    human.tm_year-=1900;

    res = div(unix_time, 86400);
    human.tm_mday = res.quot + 1;
    human.tm_wday += res.quot;
    human.tm_wday %= 7;
    human.tm_yday += res.quot;
    unix_time = res.rem;

    res = div(unix_time, 3600);
    human.tm_hour = res.quot;
    unix_time = res.rem;

    res = div(unix_time, 60);
    human.tm_min = res.quot;
    unix_time = res.rem;

    human.tm_sec = unix_time;

    return human;
}


struct tm time_;
struct tm *gmtime(time_t *timer){
    time_t unix_time;
    struct tm human;
    unix_time = *timer;
    time_ = unix_to_human(unix_time); 
    return &time_;
}

struct tm *localtime(const time_t *timer){
    time_t unix_time, local_time;
    time_t dst_offset = 0;
    struct tm human;

    unix_time = *timer;
    if (_is_dst_unix(unix_time)){
	    dst_offset = 3600;
    }
    local_time = unix_time + tz_offset + dst_offset;
    time_ = unix_to_human(local_time);
    time_.tm_isdst = _is_dst_unix(unix_time);
    return &time_;
}

///4.12.3.5 The strftime function
//TODO
