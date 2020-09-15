#ifndef __STRING_H__
#define __STRING_H__

/* Copy operations */

char *strcpy(char *to, const char *from);
char *strncpy(char *to, char *from, unsigned n);
void *memcpy(void * to, void *from, unsigned n);
void *memmove(void * to, void * from, unsigned n);

/* Miscellaneous String Operations */

unsigned strlen(char s[]);
void *memset(void * s, unsigned value, unsigned n);

/* String Concatenation Operations */

char *strcat(char *a, const char *b);
char *strncat(char * a, const char *b, unsigned n);

/* String Comparison Operations */

unsigned strcmp(const char *a, const char *b);
int strncmp(const char *a, const char *b, unsigned n);
int memcmp(const void* str1, const void * str2, unsigned n);

/* String Search Operations */

/* return the position of character f in string s starting from start of s */
char *strchr(const char * s, int f);

/* return the position of character f in string s starting from end of s */
char *strrchr(const char * s, char f);

/* return the number of characters at the start of string a that contain any character in string b */
unsigned strspn(const char *a, const char *b);

/* return the number of characters at the start of string a that do not contain any character in b */
unsigned strcspn(const char *a, const char *b);

/* return first occurrence of the any character in string b within string a */
/* return -1 if not found */
unsigned strpbrk(const char *a, const char *b);

/* return first occurrence of the whole of string b within string a */
/* return -1 if not found */
unsigned strstr(const char *a, const char *b);

#endif
