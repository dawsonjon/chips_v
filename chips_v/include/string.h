#ifndef __STRING_H__
#define __STRING_H__
/* Copy operations */

/*
The memcpy function

Synopsis

         #include <string.h>
         void *memcpy(void *s1, const void *s2, size_t n);

Description

   The memcpy function copies n characters from the object pointed to
by s2 into the object pointed to by s1 .  If copying takes place
between objects that overlap, the behavior is undefined.

Returns

   The memcpy function returns the value of s1 .

*/

void *memcpy(void *to, const void *from, unsigned len);

/*
The memmove function

Synopsis

         #include <string.h>
         void *memmove(void *s1, const void *s2, size_t n);

Description

   The memmove function copies n characters from the object pointed to
by s2 into the object pointed to by s1 .  Copying takes place as if
the n characters from the object pointed to by s2 are first copied
into a temporary array of n characters that does not overlap the
objects pointed to by s1 and s2 , and then the n characters from the
temporary array are copied into the object pointed to by s1 .

Returns

   The memmove function returns the value of s1 .

*/

void *memmove(void *to, void *from, unsigned n);

/*

The strcpy function

Synopsis

         #include <string.h>
         char *strcpy(char *s1, const char *s2);

Description

   The strcpy function copies the string pointed to by s2 (including
the terminating null character) into the array pointed to by s1 .  If
copying takes place between objects that overlap, the behavior is
undefined.

Returns

   The strcpy function returns the value of s1 .

*/

char *strcpy(char *to, const char *from);

/*
The strncpy function

Synopsis

         #include <string.h>
         char *strncpy(char *s1, const char *s2, size_t n);

Description

   The strncpy function copies not more than n characters (characters
that follow a null character are not copied) from the array pointed to
by s2 to the array pointed to by s1 ./120/ If copying takes place
between objects that overlap, the behavior is undefined.

   If the array pointed to by s2 is a string that is shorter than n
characters, null characters are appended to the copy in the array
pointed to by s1 , until n characters in all have been written.

Returns

   The strncpy function returns the value of s1 .

*/

char *strncpy(char *to, const char *from, unsigned len);

/* String Concatenation Operations */

/*
The strcat function

Synopsis

         #include <string.h>
         char *strcat(char *s1, const char *s2);

Description

   The strcat function appends a copy of the string pointed to by s2
(including the terminating null character) to the end of the string
pointed to by s1 .  The initial character of s2 overwrites the null
character at the end of s1 .  If copying takes place between objects
that overlap, the behavior is undefined.

Returns

   The strcat function returns the value of s1 .

*/

char *strcat(char *a, const char *b);

/*
The strncat function

Synopsis

         #include <string.h>
         char *strncat(char *s1, const char *s2, size_t n);

Description

   The strncat function appends not more than n characters (a null
character and characters that follow it are not appended) from the
array pointed to by s2 to the end of the string pointed to by s1 .
The initial character of s2 overwrites the null character at the end
of s1 .  A terminating null character is always appended to the
result./121/ If copying takes place between objects that overlap, the
behavior is undefined.

Returns

   The strncat function returns the value of s1 .
*/

char *strncat(char *a, const char *b, unsigned n);

/* String Comparison Operations */

/*
The memcmp function

Synopsis

         #include <string.h>
         int memcmp(const void *s1, const void *s2, size_t n);

Description

   The memcmp function compares the first n characters of the object
pointed to by s1 to the first n characters of the object pointed to by
s2 ./122/

Returns

   The memcmp function returns an integer greater than, equal to, or
less than zero, according as the object pointed to by s1 is greater
than, equal to, or less than the object pointed to by s2 .

*/

int memcmp(const void *str1, const void *str2, unsigned n);

/*
The strcmp function

Synopsis

         #include <string.h>
         int strcmp(const char *s1, const char *s2);

Description

   The strcmp function compares the string pointed to by s1 to the
string pointed to by s2 .

Returns

   The strcmp function returns an integer greater than, equal to, or
less than zero, according as the string pointed to by s1 is greater
than, equal to, or less than the string pointed to by s2 .

*/

int strcmp(const char *a, const char *b);

/*

The strncmp function

Synopsis

         #include <string.h>
         int strncmp(const char *s1, const char *s2, size_t n);

Description

   The strncmp function compares not more than n characters
(characters that follow a null character are not compared) from the
array pointed to by s1 to the array pointed to by s2 .

Returns

   The strncmp function returns an integer greater than, equal to, or
less than zero, according as the possibly null-terminated array
pointed to by s1 is greater than, equal to, or less than the possibly
null-terminated array pointed to by s2 .
*/

int strncmp(const char *a, const char *b, unsigned n);

/*
The memchr function

Synopsis

         #include <string.h>
         void *memchr(const void *s, int c, size_t n);

Description

   The memchr function locates the first occurrence of c (converted to
an unsigned char ) in the initial n characters (each interpreted as
unsigned char ) of the object pointed to by s .

Returns

   The memchr function returns a pointer to the located character, or
a null pointer if the character does not occur in the object.
*/

const void *memchr(const void *s, int f, unsigned n);

/* String Search Operations */

/*
The strchr function

Synopsis

         #include <string.h>
         char *strchr(const char *s, int c);

Description

   The strchr function locates the first occurrence of c (converted to
a char ) in the string pointed to by s .  The terminating null
character is considered to be part of the string.

*/

const char *strchr(const char *s, int f);

/*
The strrchr function

Synopsis

         #include <string.h>
         char *strrchr(const char *s, int c);

Description

   The strrchr function locates the last occurrence of c (converted to
a char ) in the string pointed to by s .  The terminating null
character is considered to be part of the string.

Returns

   The strrchr function returns a pointer to the character, or a null
pointer if c does not occur in the string.
*/

const char *strrchr(const char *s, int f);

/*
The strspn function

Synopsis

         #include <string.h>
         size_t strspn(const char *s1, const char *s2);

Description

   The strspn function computes the length of the maximum initial
segment of the string pointed to by s1 which consists entirely of
characters from the string pointed to by s2 .

Returns

   The strspn function returns the length of the segment.
*/

unsigned strspn(const char *a, const char *b);

/*
The strcspn function

Synopsis

         #include <string.h>
         size_t strcspn(const char *s1, const char *s2);

Description

   The strcspn function computes the length of the maximum initial
segment of the string pointed to by s1 which consists entirely of
characters not from the string pointed to by s2 .

Returns

   The strcspn function returns the length of the segment.

*/

unsigned strcspn(const char *a, const char *b);

/*
The strpbrk function

Synopsis

         #include <string.h>
         char *strpbrk(const char *s1, const char *s2);

Description

   The strpbrk function locates the first occurrence in the string
pointed to by s1 of any character from the string pointed to by s2 .

Returns

   The strpbrk function returns a pointer to the character, or a null
pointer if no character from s2 occurs in s1 .
*/

const char *strpbrk(const char *a, const char *b);

/*
The strstr function

Synopsis

         #include <string.h>
         char *strstr(const char *s1, const char *s2);

Description

   The strstr function locates the first occurrence in the string
pointed to by s1 of the sequence of characters (excluding the
terminating null character) in the string pointed to by s2

Returns

   The strstr function returns a pointer to the located string, or a
null pointer if the string is not found.  If s2 points to a string
with zero length, the function returns s1 .

*/

const char *strstr(const char *a, const char *b);

/* Miscellaneous String Operations */

/*

The strlen function

Synopsis

         #include <string.h>
         size_t strlen(const char *s);

Description

   The strlen function computes the length of the string pointed to by s .

Returns

   The strlen function returns the number of characters that precede
the terminating null character.

*/

unsigned strlen(const char *s);

/*

The memset function

Synopsis

         #include <string.h>
         void *memset(void *s, int c, size_t n);

Description

   The memset function copies the value of c (converted to an unsigned
char ) into each of the first n characters of the object pointed to by
s .

Returns

   The memset function returns the value of s .

*/

void *memset(void *s, unsigned value, unsigned n);

#endif
