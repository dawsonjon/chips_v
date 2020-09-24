#ifndef __print__h_
#define __print__h_

#include <stdio.h>

void fprint_uhex(unsigned uhex, int width, FILE handle);
void fprint_udecimal(unsigned udecimal, int width, FILE handle);
void fprint_hex(int hex, int width, FILE handle);
void fprint_decimal(int decimal, int width, FILE handle);
void fprint_float(float f, FILE handle);
void fprint_double(double f, FILE handle);
void print_uhex(int hex, int width);
void print_udecimal(int decimal, int width);
void print_hex(int hex, int width);
void print_decimal(int decimal, int width);
void print_float(float f);
void print_double(double f);

#endif
