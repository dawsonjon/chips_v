#ifndef __STDIO_H
#define __STDIO_H

#define FILE unsigned
#include  <stdarg.h> /* for va_list */

extern const unsigned stdin;
extern const unsigned stdout;
extern const unsigned stderr;

unsigned fgetc(FILE handle);


/* putc and getc */
#define getc(handle) fgetc(handle)
#define getchar() fgetc(stdin)
int fputc(int c, FILE handle);
#define putc(c, handle) fputc(c, handle)
#define putchar(c) fputc(c, stdout)
int fputs(const char * string, FILE handle);
int puts(const char * string);
char * fgets(char * string, int maxlength, FILE handle);
char * gets(const char * string, unsigned maxlength);

/* printf and friends */
int vfprintf(FILE output, char fmt_str[], va_list ap);
int vprintf(char fmt_str[], va_list ap);
int vsprintf(char * buffer, char fmt_str[], va_list ap);
int fprintf(FILE output, char fmt_str[], ...);
int printf(char fmt_str[], ...);
int sprintf(char * buffer, char fmt_str[], ...);

#endif

