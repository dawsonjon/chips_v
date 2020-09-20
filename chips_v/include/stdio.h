#ifndef __STDIO_H
#define __STDIO_H

#define FILE unsigned
#include <printf.h>

extern const unsigned stdin;
extern const unsigned stdout;
extern const unsigned stderr;

unsigned fgetc(FILE handle);

/* putc and getc */
unsigned fgetc(FILE handle);
unsigned getc(FILE handle);
int getchar();

int fputc(int c, FILE handle);
int putc(int c, FILE handle);
int putchar(int c);

int fputs(const char *string, FILE handle);
int puts(const char *string);

char *fgets(char *string, int maxlength, FILE handle);
char *gets(const char *string, unsigned maxlength);

#endif
