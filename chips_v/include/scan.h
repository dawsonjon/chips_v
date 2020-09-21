#ifndef __scan_h__
#define __scan_h__
#include <ctype.h>
#include <stdio.h>

unsigned hex2nibble_(char hex);
unsigned fscan_uhex(unsigned f);
unsigned fscan_udecimal(unsigned f);
int fscan_hex(unsigned f);
int fscan_decimal(unsigned f);
float fscan_float(unsigned f);
double fscan_double(unsigned f);
unsigned scan_uhex();
unsigned scan_udecimal();
int scan_hex();
int scan_decimal();
float scan_float();
double scan_double();

#endif
